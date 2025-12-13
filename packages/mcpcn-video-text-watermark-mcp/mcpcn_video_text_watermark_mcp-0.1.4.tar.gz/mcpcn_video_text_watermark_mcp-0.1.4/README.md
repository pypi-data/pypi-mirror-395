# Video Text Watermark MCP

A Model Context Protocol (MCP) server for adding text watermarks and overlays to videos.

## Features

- **Text Watermark**: Add permanent text watermarks to videos
- **Text Overlay**: Add timed text overlays that appear during specific time ranges
- Support for Chinese and other Unicode characters
- Customizable font, color, size, position, and opacity
- Background box support

## Installation

Install via uvx (recommended):

```bash
uvx video-text-watermark-mcp
```

Or install via pip:

```bash
pip install video-text-watermark-mcp
```

## Usage

Run the MCP server:

```bash
video-text-watermark-mcp
```

## Requirements

- Python >=3.12
- FFmpeg installed on your system

## Tools

### `add_text_watermark`

Add a permanent text watermark to video:
- `video_path`: Input video file path
- `output_video_path`: Output video file path
- `watermark_text`: Text content
- `font_size`: Font size (default 24)
- `font_color`: Font color (default 'white')
- `position`: Position preset or custom coordinates
- `opacity`: Transparency (0.0-1.0)
- `font_file`: Custom font file path
- `box`: Enable background box

### `add_text_overlay`

Add timed text overlays:
- `video_path`: Input video file path
- `output_video_path`: Output video file path
- `text_elements`: List of text overlay configurations

## License

MIT License
