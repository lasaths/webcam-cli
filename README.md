<div align="center">

# Webcam MCP 📸

**MCP server for webcam access - capture photos and video for LLM agents**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## Overview

Webcam MCP is a Model Context Protocol (MCP) server that gives LLM agents direct access to your webcam. It enables autonomous agents to capture photos and record video sequences, making it possible to debug cyberphysical systems, monitor environments, and interact with the physical world without human intervention.

## Features

- **📸 High-Resolution Photos**: Capture Full HD (1920x1080) images
- **🎥 Video Recording**: Record up to 50 frames over a specified duration (480p)
- **🌐 Remote Access**: SSE transport for network-accessible deployment
- **⚙️ Configurable**: Adjust resolution, camera index, and quality settings
- **🔌 Cross-Platform**: Works on Linux, macOS, and Windows
- **🚀 Easy Integration**: Simple MCP client configuration

## Installation

```bash
pip install webcam-mcp
```

## Quick Start

Start the MCP server:

```bash
webcam-mcp
```

The server will start on `http://0.0.0.0:8000/sse` by default.

## CLI Reference

```bash
webcam-mcp [OPTIONS]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--host` | string | `0.0.0.0` | Server host address |
| `--port` | integer | `8000` | Server port |
| `--camera-index` | integer | `0` | Webcam device index |
| `--photo-width` | integer | `1920` | Default photo width in pixels |
| `--photo-height` | integer | `1080` | Default photo height in pixels |
| `--video-width` | integer | `640` | Default video frame width in pixels |
| `--video-height` | integer | `480` | Default video frame height in pixels |
| `--version` | - | - | Show version and exit |

### Examples

```bash
# Start on custom port
webcam-mcp --port 9000

# Use different camera (e.g., external USB webcam)
webcam-mcp --camera-index 1

# Custom photo resolution
webcam-mcp --photo-width 1280 --photo-height 720
```

## MCP Client Configuration

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "webcam": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

**Location of config file:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

### Other MCP Clients

Any MCP client supporting SSE transport can connect to:

```
http://<host>:<port>/sse
```

## MCP Tools

### `take_photo`

Captures a single high-resolution photo from the webcam.

**Parameters:** None

**Returns:** JPEG image (default: 1920x1080, quality 90)

**Example usage in Claude:**
```
Can you take a photo and describe what you see?
```

### `record_video`

Records video frames over a specified duration.

**Parameters:**
- `duration_seconds` (float, optional): Recording duration in seconds (default: 5.0)
  - Minimum: 1.0 second
  - Maximum: 60.0 seconds

**Returns:** List of up to 50 JPEG frames (default: 640x480, quality 90)

**Example usage in Claude:**
```
Record a 10-second video and analyze any movement you detect.
```

## Troubleshooting

### Camera Permission Denied (macOS)

On macOS, you need to grant camera permissions:

1. Open **System Settings** → **Privacy & Security** → **Camera**
2. Enable camera access for **Terminal** (or your terminal app)
3. Restart the terminal and try again

### Camera Already in Use

If you see "Camera unavailable" errors:

1. Close other applications using the webcam (Zoom, Skype, etc.)
2. Check if another instance of `webcam-mcp` is running
3. Try a different camera index: `webcam-mcp --camera-index 1`

### Wrong Camera Index

To find available cameras:

```python
import cv2
for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i}: Available")
        cap.release()
    else:
        print(f"Camera {i}: Not available")
```

Then use `--camera-index` with the correct number.

### Resolution Not Supported

If your camera doesn't support the requested resolution, the server will:
- Log a warning with the actual resolution achieved
- Continue operating with the camera's maximum supported resolution

Check logs for messages like:
```
WARNING: Requested resolution 1920x1080, but camera provided 1280x720
```

## Development

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd webcam-mcp

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_camera.py
```

All tests use mocked camera hardware, so no physical webcam is required for testing.

### Project Structure

```
webcam-mcp/
├── src/webcam_mcp/
│   ├── __init__.py      # Package version
│   ├── camera.py        # Webcam capture logic
│   ├── server.py        # FastMCP server and tools
│   ├── cli.py           # Command-line interface
│   └── config.py        # Configuration dataclass
├── tests/               # Test suite
├── pyproject.toml       # Package configuration
└── README.md           # This file
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

**Built with [FastMCP](https://github.com/modelcontextprotocol/python-sdk)** | **Powered by OpenCV**
