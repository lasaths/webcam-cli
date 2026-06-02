"""Command-line interface for Webcam MCP server."""

import argparse
from pathlib import Path

from webcam_mcp import __version__
from webcam_mcp.camera import WebcamCapture, WebcamError
from webcam_mcp.config import ServerConfig
from webcam_mcp.server import create_server


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        args: List of arguments to parse (defaults to sys.argv[1:])

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        prog="webcam-mcp",
        description="MCP server for webcam access",
    )

    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Server host (default: 0.0.0.0)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Server port (default: 8000)",
    )

    parser.add_argument(
        "--camera-index",
        type=int,
        default=0,
        help="Webcam index (default: 0)",
    )

    parser.add_argument(
        "--photo-width",
        type=int,
        default=1920,
        help="Default photo width (default: 1920)",
    )

    parser.add_argument(
        "--photo-height",
        type=int,
        default=1080,
        help="Default photo height (default: 1080)",
    )

    parser.add_argument(
        "--video-width",
        type=int,
        default=640,
        help="Default video width (default: 640)",
    )

    parser.add_argument(
        "--video-height",
        type=int,
        default=480,
        help="Default video height (default: 480)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"webcam-mcp {__version__}",
    )

    parser.add_argument(
        "--transport",
        type=str,
        default="stdio",
        choices=["stdio", "sse"],
        help="Transport: 'stdio' for Copilot/CLI tools, 'sse' for HTTP server (default: stdio)",
    )

    parser.add_argument(
        "--capture-photo",
        type=str,
        default=None,
        help="Capture a single photo to this output path and exit",
    )

    parser.add_argument(
        "--autofocus-seconds",
        type=float,
        default=2.0,
        help="Autofocus warm-up time before single-photo capture (default: 2.0)",
    )

    return parser.parse_args(args)


def main(args: list[str] | None = None) -> None:
    """Main entry point for the CLI.

    Parses arguments, creates server configuration, and runs the server.

    Args:
        args: List of arguments to parse (defaults to sys.argv[1:])
    """
    parsed_args = parse_args(args)

    if parsed_args.capture_photo:
        output_path = Path(parsed_args.capture_photo).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        def _capture_with_index(index: int) -> bytes:
            camera = WebcamCapture(index)
            return camera.capture_photo(
                width=parsed_args.photo_width,
                height=parsed_args.photo_height,
                quality=90,
                autofocus_seconds=parsed_args.autofocus_seconds,
            )

        try:
            jpeg_bytes = _capture_with_index(parsed_args.camera_index)
        except WebcamError:
            if parsed_args.camera_index != 0:
                raise
            jpeg_bytes = _capture_with_index(1)

        output_path.write_bytes(jpeg_bytes)
        print(str(output_path))
        return

    config = ServerConfig(
        camera_index=parsed_args.camera_index,
        photo_width=parsed_args.photo_width,
        photo_height=parsed_args.photo_height,
        video_width=parsed_args.video_width,
        video_height=parsed_args.video_height,
        host=parsed_args.host,
        port=parsed_args.port,
    )

    server = create_server(config)
    server.run(transport=parsed_args.transport)


if __name__ == "__main__":
    main()
