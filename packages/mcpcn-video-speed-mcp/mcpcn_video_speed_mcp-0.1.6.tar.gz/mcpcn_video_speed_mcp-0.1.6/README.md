# Video Speed MCP

A Model Context Protocol (MCP) server for changing video playback speed with proper audio sync.

## Features

- **Speed Control**: Adjust video playback speed
- Supports both fast-forward (>1x) and slow-motion (<1x)
- Proper audio pitch correction using atempo filter
- Handles extreme speed changes (very slow or very fast)
- Audio and video remain synchronized

## Installation

Install via uvx (recommended):

```bash
uvx video-speed-mcp
```

Or install via pip:

```bash
pip install video-speed-mcp
```

## Usage

Run the MCP server:

```bash
video-speed-mcp
```

## Requirements

- Python >=3.12
- FFmpeg installed on your system

## Tool

### `change_video_speed`

Change video playback speed:
- `video_path`: Input video file path
- `output_video_path`: Output video file path
- `speed_factor`: Speed multiplier (e.g., 2.0 for 2x speed, 0.5 for half speed)

### Examples

- `speed_factor=2.0`: Double speed (video plays 2x faster)
- `speed_factor=0.5`: Half speed (slow motion)
- `speed_factor=1.5`: 1.5x speed
- `speed_factor=0.25`: Quarter speed (very slow motion)
- `speed_factor=4.0`: 4x speed (very fast)

## License

MIT License