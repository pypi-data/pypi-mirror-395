"""
Video Cover MCP Server

A MCP server for adding cover images and fade transitions to videos including:
- Add cover image (first frame) to video beginning
- Fade-in and fade-out transition effects
- Configurable cover duration and transition timing
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .main import main

__all__ = ["main"]
