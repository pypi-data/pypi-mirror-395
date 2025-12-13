"""
upserver - A resumable file server for uploading and downloading files.

This package provides a robust and efficient way to set up a file server
with resumable chunked uploads, web interface, and file management capabilities.

Features:
- Resumable chunked file uploads
- Web interface for file management
- Real-time upload progress tracking
- File listing and download
- Cross-platform compatibility
- Configurable logging and settings
"""

__version__ = "0.2.0"
__author__ = "Álex Vieira"
__license__ = "MIT"

from .server import FileServer
from .config import ServerConfig
from .logging_config import setup_logging, ServerLogger
from .utils import sanitize_filename, get_disk_space, format_file_size

__all__ = [
    "FileServer",
    "ServerConfig",
    "setup_logging",
    "ServerLogger",
    "sanitize_filename",
    "get_disk_space",
    "format_file_size",
]
