# Video Cover MCP

A Model Context Protocol (MCP) server for adding cover images (first frame) and fade transitions to videos.

## Features

- **Add Cover Image**: Prepend a static image as the video's cover/intro
- **Fade Transitions**: Add fade-in and fade-out effects to videos
- **Flexible Duration**: Configure cover display duration and transition timing

## Installation

Install via uvx (recommended):

```bash
uvx video-cover-mcp
```

Or install via pip:

```bash
pip install video-cover-mcp
```

## Usage

Run the MCP server:

```bash
video-cover-mcp
```

## Requirements

- Python >=3.12
- FFmpeg installed on your system

## Tools Available

### `add_cover_image`

Add a cover image (first frame) to the beginning of a video.

**Parameters:**
- `video_path`: Input video file path
- `cover_image_path`: Cover image file path (supports PNG, JPG, etc.)
- `output_video_path`: Output video file path
- `cover_duration`: Duration to display the cover image in seconds (default: 3.0)
- `fade_duration`: Fade transition duration in seconds (default: 0.5)

**Example:**
```python
add_cover_image(
    video_path="/path/to/input.mp4",
    cover_image_path="/path/to/cover.jpg",
    output_video_path="/path/to/output.mp4",
    cover_duration=5.0,
    fade_duration=1.0
)
```

### `add_basic_transitions`

Add fade-in or fade-out transition effects to a video.

**Parameters:**
- `video_path`: Input video file path
- `output_video_path`: Output video file path
- `transition_type`: Transition type - 'fade_in' or 'fade_out'
- `duration_seconds`: Transition duration in seconds (must be positive)

**Example:**
```python
add_basic_transitions(
    video_path="/path/to/input.mp4",
    output_video_path="/path/to/output.mp4",
    transition_type="fade_in",
    duration_seconds=2.0
)
```

## License

MIT License