# Video Trim MCP

按时间范围裁剪视频片段的 MCP Server。

## 功能

- 按指定时间范围裁剪视频
- 优先使用 codec copy 避免重编码
- 支持 HH:MM:SS 或秒数格式的时间输入

## 安装

```bash
uvx video-trim-mcp
```

或通过 pip 安装：

```bash
pip install video-trim-mcp
```

## 使用

```bash
video-trim-mcp
```

## 工具

### trim_video

按指定时间范围裁剪视频片段。

**参数：**
- `video_path`: 输入视频文件路径
- `output_video_path`: 输出视频文件路径
- `start_time`: 开始时间（支持 'HH:MM:SS' 或秒数）
- `end_time`: 结束时间（支持 'HH:MM:SS' 或秒数）

## 依赖

- Python >=3.12
- FFmpeg（需系统安装）

## License

MIT License