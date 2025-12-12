# 视频-AI加字幕 MCP Server

MCP server for AI-powered video subtitle generation and merging using Volcano Engine speech recognition.

## Features

- **generate_subtitle**: Generate SRT subtitle file from video URL using AI speech recognition
- **merge_subtitle**: Burn subtitles into video with customizable styling (color, size, position)

## Installation

```bash
pip install mcpcn-video-ai-subtitle-mcp
```

## Environment Variables

- `VOLCANO_APPID`: Volcano Engine App ID
- `VOLCANO_ACCESS_TOKEN`: Volcano Engine Access Token
- `FFMPEG_BINARY`: (Optional) Path to ffmpeg binary
- `FFPROBE_BINARY`: (Optional) Path to ffprobe binary

## Usage

### MCP Configuration

```json
{
  "mcpServers": {
    "video-ai-subtitle": {
      "command": "uvx",
      "args": ["mcpcn-video-ai-subtitle-mcp"],
      "env": {
        "VOLCANO_APPID": "your-app-id",
        "VOLCANO_ACCESS_TOKEN": "your-access-token"
      }
    }
  }
}
```

## License

MIT
