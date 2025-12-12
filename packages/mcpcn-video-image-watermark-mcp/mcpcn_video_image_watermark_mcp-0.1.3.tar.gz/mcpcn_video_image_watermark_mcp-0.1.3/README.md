# Video Image Watermark MCP

A Model Context Protocol (MCP) server for adding image watermarks and overlays to videos.

## Features

- **Image Overlay**: Add logos, watermarks, or any image to videos
- Support for transparent PNG images
- Customizable position, size, and opacity
- Timed overlays with start/end time support
- Automatic aspect ratio preservation

## Installation

Install via uvx (recommended):

```bash
uvx video-image-watermark-mcp
```

Or install via pip:

```bash
pip install video-image-watermark-mcp
```

## Usage

Run the MCP server:

```bash
video-image-watermark-mcp
```

## Requirements

- Python >=3.12
- FFmpeg installed on your system

## Tool

### `add_image_overlay`

Add image overlay to video:
- `video_path`: Input video file path
- `output_video_path`: Output video file path
- `image_path`: Overlay image path (supports transparent PNG)
- `position`: Position preset ('top_left', 'top_right', 'bottom_left', 'bottom_right', 'center') or custom 'x=...:y=...'
- `opacity`: Transparency (0.0-1.0)
- `start_time`: When to start showing the overlay
- `end_time`: When to stop showing the overlay
- `width`: Target width (auto-calculates height if not specified)
- `height`: Target height (auto-calculates width if not specified)

## License

MIT License
