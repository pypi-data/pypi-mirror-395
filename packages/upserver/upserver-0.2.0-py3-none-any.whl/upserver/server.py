"""
Main server module for file upload and download functionality.
"""

import sys

from datetime import datetime
from http.server import HTTPServer
from pathlib import Path

from .handlers import ResumableUploadHandler
from .utils import get_disk_space, ensure_directory_exists, get_system_info


class FileServer:
    """
    A resumable file server that handles chunked uploads and downloads.

    Features:
    - Resumable chunked file uploads
    - Web interface for file management
    - File listing and download
    - Real-time upload progress
    - Cross-platform compatibility

    Attributes:
        upload_dir (Path): Directory where uploaded files are stored
        temp_dir (Path): Directory for temporary upload chunks
        host (str): Server host address
        port (int): Server port number
        chunk_size (int): Size of upload chunks in bytes
    """

    def __init__(
        self,
        upload_dir="uploads",
        host="0.0.0.0",  # nosec B104 - intentional for file server access
        port=8000,
        chunk_size=5 * 1024 * 1024,
    ):
        """
        Initialize the file server.

        Args:
            upload_dir (str): Directory to store uploaded files
            host (str): Host address to bind the server
            port (int): Port number to bind the server
            chunk_size (int): Size of upload chunks in bytes (default: 5MB)
        """
        self.upload_dir = ensure_directory_exists(upload_dir)
        self.temp_dir = ensure_directory_exists(self.upload_dir / "temp")
        self.host = host
        self.port = port
        self.chunk_size = chunk_size
        self.server = None

    def start(self):
        """
        Start the HTTP server with resumable upload capability.

        The server provides:
        - Web interface for file uploads at /
        - File listing endpoint at /files
        - File download endpoint at /download/{filename}
        - Chunked upload endpoint at /upload
        """
        # Display startup information
        self._print_startup_info()

        # Create custom handler class with server configuration
        file_server = self  # Reference to the FileServer instance

        class ConfiguredHandler(ResumableUploadHandler):
            def __init__(self, request, client_address, server):
                # Inject server configuration into handler
                server.upload_dir = str(file_server.upload_dir)
                server.temp_dir = str(file_server.temp_dir)
                server.chunk_size = file_server.chunk_size
                super().__init__(request, client_address, server)

        # Start HTTP server
        self.server = HTTPServer((self.host, self.port), ConfiguredHandler)

        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] ⚡ Server running and listening for requests...\n")
            sys.stdout.flush()
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """
        Stop the server gracefully.
        """
        print("\n\n🛑 Interrupt detected - Stopping server...")
        if self.server:
            self.server.shutdown()
        print("✅ Server stopped successfully!\n")
        sys.stdout.flush()

    def _print_startup_info(self):
        """
        Print detailed startup information.
        """
        total_gb, used_gb, free_gb = get_disk_space(self.upload_dir)
        system_info = get_system_info()

        print("\n" + "=" * 70)
        print("🚀 RESUMABLE HTTP FILE SERVER + LISTING/DOWNLOAD")
        print("=" * 70)
        print(f"📅 Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🖥️  System: {system_info['system']} {system_info['release']}")
        print(f"🐍 Python: {system_info['python_version']}")
        host_display = (
            self.host if self.host != "0.0.0.0" else "localhost"
        )  # nosec B104
        print(f"📍 URL: http://{host_display}:{self.port}")
        print(f"📁 Upload Directory: {self.upload_dir}")
        print(f"📁 Temp Directory: {self.temp_dir}")
        print(f"💾 Total Space: {total_gb:.2f} GB")
        print(f"💾 Used Space: {used_gb:.2f} GB")
        print(f"💾 Free Space: {free_gb:.2f} GB")
        print(f"📦 Chunk Size: {self.chunk_size / (1024*1024):.1f} MB")
        print("🔄 Resumable: YES")
        print("⏸️ Pause/Resume: YES")
        print("📂 Accepts: ANY FILE TYPE")
        print("=" * 70)
        print("\n🟢 SERVER ONLINE AND READY FOR UPLOADS")
        print("👀 Waiting for connections...")
        host_display = (
            self.host if self.host != "0.0.0.0" else "localhost"
        )  # nosec B104
        print(
            f"💡 Tip: Open http://{host_display}:{self.port} "
            f"in browser to upload, list and download files"
        )
        print("🛑 Press Ctrl+C to stop the server\n" + "=" * 70)
        sys.stdout.flush()

    def upload_file(self, file_data, filename):
        """
        Upload a file to the server.

        Args:
            file_data (bytes): File content as bytes
            filename (str): Name of the file to save

        Returns:
            Path: Path to the saved file
        """
        # Prevent path traversal attacks by using only the filename component
        safe_filename = Path(filename).name
        file_path = self.upload_dir / safe_filename
        with open(file_path, "wb") as f:
            f.write(file_data)
        return file_path

    def download_file(self, filename):
        """
        Download a file from the server.

        Args:
            filename (str): Name of the file to download

        Returns:
            bytes: File content as bytes

        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        # Prevent path traversal attacks by using only the filename component
        safe_filename = Path(filename).name
        file_path = self.upload_dir / safe_filename
        if not file_path.exists():
            raise FileNotFoundError(f"File '{filename}' not found")

        with open(file_path, "rb") as f:
            return f.read()

    def list_files(self):
        """
        List all files in the upload directory.

        Returns:
            list: List of filenames
        """
        return [f.name for f in self.upload_dir.iterdir() if f.is_file()]
