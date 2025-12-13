# Video Silence Remover MCP

A Model Context Protocol (MCP) server for automatically removing silent segments from audio and video files.

## Features

- **Silence Detection**: Automatically detect silent segments based on configurable threshold
- **Smart Removal**: Remove silent parts while preserving audio-video sync
- **Configurable Parameters**: Adjust silence threshold, minimum duration, and padding
- **Multi-format Support**: Works with both audio and video files

## Installation

Install via uvx (recommended):

```bash
uvx video-silence-remover-mcp
```

Or install via pip:

```bash
pip install video-silence-remover-mcp
```

## Usage

Run the MCP server:

```bash
video-silence-remover-mcp
```

## Requirements

- Python >=3.12
- FFmpeg installed on your system

## Tools Available

### `remove_silence`

Remove silent segments from audio/video files.

**Parameters:**
- `media_path`: Input media file path (audio or video)
- `output_media_path`: Output media file path
- `silence_threshold_db`: Silence detection threshold in dBFS (default: -30)
- `min_silence_duration_ms`: Minimum silence duration to trigger removal in milliseconds (default: 500)
- `padding_seconds`: Buffer time to preserve before/after segments in seconds (default: 0.2)

**Example:**
```python
remove_silence(
    media_path="/path/to/input.mp4",
    output_media_path="/path/to/output.mp4",
    silence_threshold_db=-35,
    min_silence_duration_ms=1000,
    padding_seconds=0.3
)
```

## License

MIT License