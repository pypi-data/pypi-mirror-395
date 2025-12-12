# Video Aspect Ratio MCP

A Model Context Protocol (MCP) server for adjusting video aspect ratio.

## Features

- **Aspect Ratio Adjustment**: Change video aspect ratios with padding or cropping
- Support for common ratios: 16:9, 4:3, 1:1, 9:16, etc.
- Padding mode with customizable colors
- Crop mode for center cropping

## Installation

Install via uvx (recommended):

```bash
uvx video-aspect-ratio-mcp
```

Or install via pip:

```bash
pip install video-aspect-ratio-mcp
```

## Usage

Run the MCP server:

```bash
video-aspect-ratio-mcp
```

## Requirements

- Python >=3.12
- FFmpeg installed on your system

## Tool

### `change_aspect_ratio`

Adjust video aspect ratio with options:
- `video_path`: Input video file path
- `output_video_path`: Output video file path
- `target_aspect_ratio`: Target ratio (e.g., '16:9', '4:3', '1:1')
- `resize_mode`: 'pad' (scale and add borders) or 'crop' (center crop)
- `padding_color`: Border color when using pad mode (e.g., 'black', 'white', '#RRGGBB')

## License

MIT License
