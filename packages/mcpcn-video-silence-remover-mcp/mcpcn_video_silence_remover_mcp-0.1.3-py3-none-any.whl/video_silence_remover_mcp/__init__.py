"""
Video Silence Remover MCP Server

A MCP server for removing silent segments from audio/video files including:
- Silence detection based on configurable threshold
- Smart removal while preserving audio-video sync
- Configurable minimum silence duration
- Padding support for smooth transitions
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .main import main

__all__ = ["main"]
