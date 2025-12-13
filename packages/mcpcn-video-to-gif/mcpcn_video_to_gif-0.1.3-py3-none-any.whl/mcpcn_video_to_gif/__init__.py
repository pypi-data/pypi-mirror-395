"""
Video to GIF Converter MCP Server

A MCP server for converting video to high-quality GIF including:
- Two-pass palette optimization
- Custom frame rate and resolution
- Dithering algorithm selection
- Cropping and time range selection
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .server import main

__all__ = ["main"]
