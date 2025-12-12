from mcp.server.fastmcp import FastMCP, Context
import ffmpeg
import os
import logging
from logging.handlers import RotatingFileHandler
import tempfile
import subprocess
from pathlib import Path
import platform
import urllib.parse
import time


# 配置日志输出到stderr，避免干扰MCP通信
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

package = "video-extract-audio-mcp"

# 使用用户临时目录存放日志文件
log_dir = Path(tempfile.gettempdir()) / package
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "debug.log"

file_handler = RotatingFileHandler(
    str(log_file), maxBytes=5_000_000, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)
logger.propagate = False

FFMPEG_BINARY = os.environ.get("FFMPEG_BINARY")
FFPROBE_BINARY = os.environ.get("FFPROBE_BINARY")


def _ffmpeg_run(stream_spec, **kwargs):
    """Run ffmpeg with an explicit binary path."""
    if "overwrite_output" not in kwargs:
        kwargs["overwrite_output"] = True
    return ffmpeg.run(stream_spec, cmd=FFMPEG_BINARY, **kwargs)


def _prepare_path(input_path: str, output_path: str) -> None:
    """Prepare and validate input/output paths."""
    if not os.path.exists(input_path):
        raise RuntimeError(f"Error: Input file not found at {input_path}")
    try:
        parent_dir = os.path.dirname(output_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
    except Exception as e:
        raise RuntimeError(
            f"Error creating output directory for {output_path}: {str(e)}"
        )
    if os.path.exists(output_path):
        raise RuntimeError(
            f"Error: Output file already exists at {output_path}. Please choose a different path or delete the existing file."
        )


def _open_aido_link(ctx: Context, return_message: str) -> None:
    """Silently execute aido://tool?xxx&chatSessionId=xxx across platforms."""
    try:
        if ctx is None:
            logger.debug("Context is None, skipping aido link execution")
            return

        request_context = getattr(ctx, "request_context", None)
        chatSessionId = None
        if request_context and hasattr(request_context, "meta"):
            context_meta = getattr(request_context, "meta", None)
            logger.debug(f"context meta: {context_meta}")
            if context_meta and hasattr(context_meta, "chatSessionId"):
                chatSessionId = getattr(context_meta, "chatSessionId", None)
                logger.debug(
                    f"chatSessionId from request_context.meta: {chatSessionId}"
                )

        if not chatSessionId or chatSessionId == "None":
            logger.warning(
                f"Invalid or missing chatSessionId: {chatSessionId}, skipping aido link execution"
            )
            return

        encoded_message = urllib.parse.quote(return_message, safe="")
        package_name = urllib.parse.quote(package, safe="")
        aido_url = f"aido://tool?path={encoded_message}&chatSessionId={chatSessionId}&package={package_name}"

        system = platform.system().lower()
        if system == "darwin":
            result = subprocess.run(
                ["open", aido_url], check=False, capture_output=True, text=True
            )
            if result.returncode != 0 and result.stderr:
                logger.warning(f"macOS open command failed: {result.stderr}")
        elif system == "windows":
            try:
                os.startfile(aido_url)
            except (OSError, AttributeError) as e:
                logger.debug(f"os.startfile failed, trying start command: {e}")
                result = subprocess.run(
                    f'start "" "{aido_url}"',
                    shell=True,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0 and result.stderr:
                    logger.warning(f"Windows start command failed: {result.stderr}")
        elif system == "linux":
            result = subprocess.run(
                ["xdg-open", aido_url], check=False, capture_output=True, text=True
            )
            if result.returncode != 0 and result.stderr:
                logger.warning(f"Linux xdg-open command failed: {result.stderr}")
        else:
            logger.warning(f"Unsupported operating system: {system}")
            return

        logger.info(f"Executed aido link on {system}: {aido_url}")
    except Exception as e:
        logger.error(f"Failed to execute aido link: {str(e)}", exc_info=True)


mcp = FastMCP("VideoExtractAudio")


@mcp.tool()
def extract_audio_from_video(
    video_paths: list[str],
    output_dir: str,
    audio_codec: str = "mp3",
    ctx: Context = None,
) -> str:
    """Extract audio tracks from one or more video files.

    Args:
        video_paths: List of input video paths, multiple videos are supported.
        output_dir: Destination directory where each extracted audio file is saved.
        audio_codec: Output audio codec (e.g., 'mp3', 'aac', 'wav', 'flac').

    Returns:
        A status message indicating success or failure for each file.
    """
    execution_start_time = time.time()

    # 校验音频编码格式
    valid_codecs = {"mp3", "aac", "wav", "flac", "m4a", "ogg", "wma"}
    if audio_codec not in valid_codecs:
        raise RuntimeError(
            f"Error: Invalid audio_codec '{audio_codec}'. Supported: {', '.join(sorted(valid_codecs))}"
        )

    # 确保输出目录存在
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Error creating output directory {output_dir}: {str(e)}")

    results = []
    success_count = 0
    fail_count = 0
    output_files = []

    for idx, video_path in enumerate(video_paths):
        try:
            # 检查输入文件
            if not os.path.exists(video_path):
                results.append(f"[FAILED] {video_path}: File not found")
                fail_count += 1
                continue

            # 生成输出文件名
            video_filename = os.path.basename(video_path)
            video_name = os.path.splitext(video_filename)[0]
            output_audio_path = os.path.join(output_dir, f"{video_name}.{audio_codec}")

            # 检查输出文件是否已存在
            if os.path.exists(output_audio_path):
                results.append(f"[FAILED] {video_path}: Output file already exists at {output_audio_path}")
                fail_count += 1
                continue

            logger.info(
                f"Extracting audio from {video_path} to {output_audio_path} with codec {audio_codec}"
            )

            try:
                exists = os.path.exists(video_path)
                readable = os.access(video_path, os.R_OK)
                size = os.path.getsize(video_path) if exists else "N/A"
                logger.info(
                    f"Input file check: exists={exists} readable={readable} size={size}"
                )
            except Exception as _e:
                logger.info(f"Input file check failed: {str(_e)}")

            if ctx:
                progress = int((idx / len(video_paths)) * 100)
                ctx.report_progress(progress, f"Extracting audio ({idx + 1}/{len(video_paths)}): {video_filename}")

            # 检查视频是否包含音频流
            try:
                probe = ffmpeg.probe(video_path, cmd=FFPROBE_BINARY)
                audio_streams = [s for s in probe['streams'] if s['codec_type'] == 'audio']
                
                if not audio_streams:
                    results.append(f"[SKIPPED] {video_path}: Video has no audio stream")
                    fail_count += 1
                    continue
            except ffmpeg.Error as probe_error:
                error_message = probe_error.stderr.decode("utf8") if probe_error.stderr else str(probe_error)
                results.append(f"[FAILED] {video_path}: Unable to probe video - {error_message}")
                fail_count += 1
                continue

            input_stream = ffmpeg.input(video_path)
            output_stream = input_stream.output(output_audio_path, acodec=audio_codec)
            _ffmpeg_run(output_stream, capture_stdout=True, capture_stderr=True)

            results.append(f"[SUCCESS] {video_path} -> {output_audio_path}")
            output_files.append(output_audio_path)
            success_count += 1

        except ffmpeg.Error as e:
            error_message = e.stderr.decode("utf8") if e.stderr else str(e)
            results.append(f"[FAILED] {video_path}: {error_message}")
            fail_count += 1
        except FileNotFoundError as e:
            msg = str(e)
            logger.info(f"FileNotFoundError: {msg}")
            if FFMPEG_BINARY and (
                FFMPEG_BINARY in msg or os.path.basename(FFMPEG_BINARY) in msg
            ):
                results.append(f"[FAILED] {video_path}: ffmpeg executable not found. FFMPEG_BINARY={FFMPEG_BINARY}")
            else:
                results.append(f"[FAILED] {video_path}: File not found")
            fail_count += 1
        except Exception as e:
            results.append(f"[FAILED] {video_path}: {str(e)}")
            fail_count += 1

    # 计算执行时间
    execution_time = time.time() - execution_start_time

    # 构建返回消息
    result_message = f"Audio extraction completed. Success: {success_count}, Failed: {fail_count}. Execution time: {execution_time:.2f} seconds.\n\nDetails:\n" + "\n".join(results)

    # 如果全部失败，抛出异常以设置 isError: true
    if success_count == 0 and fail_count > 0:
        raise RuntimeError(result_message)

    # 只有执行时间超过1秒且有成功的文件才调用 _open_aido_link
    if execution_time > 59 and output_files:
        for path in output_files:
            _open_aido_link(ctx, path)

    return result_message


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
