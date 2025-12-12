# Video Extract Audio MCP

从视频文件中提取音频的 MCP Server。

## 功能

- 从视频文件提取音频轨道
- 支持多种音频格式：mp3、aac、wav、flac、m4a、ogg、wma

## 安装

```bash
uvx video-extract-audio-mcp
```

或通过 pip 安装：

```bash
pip install video-extract-audio-mcp
```

## 使用

```bash
video-extract-audio-mcp
```

## 工具

### extract_audio_from_video

从视频文件中提取音频。

**参数：**
- `video_path`: 输入视频文件路径
- `output_audio_path`: 输出音频文件路径
- `audio_codec`: 音频编码格式（默认 'mp3'）

## 依赖

- Python >=3.12
- FFmpeg（需系统安装）

## License

MIT License