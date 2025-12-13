"""
HTTP request handlers for the upserver package.
"""

import os
import json
import time
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler


from .utils import sanitize_filename
from .templates import get_upload_page_html


class ResumableUploadHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for resumable file uploads with web interface.

    This handler provides:
    - Resumable chunked file uploads
    - File listing and download
    - Web interface for file management
    - Real-time upload progress tracking
    """

    # Class variables for request tracking
    request_counter = 0
    request_lock = threading.Lock()

    def __init__(self, request, client_address, server):
        """
        Initialize the handler with server configuration.
        """
        self.upload_dir = getattr(server, "upload_dir", "./uploads")
        self.temp_dir = getattr(server, "temp_dir", "./uploads/temp")
        self.chunk_size = getattr(server, "chunk_size", 5 * 1024 * 1024)  # 5MB
        super().__init__(request, client_address, server)

    def log_message(self, format_string, *args):
        """
        Custom logging with timestamps.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] {format_string % args}")

    def do_GET(self):
        """
        Handle GET requests for file listing, downloads, and web interface.
        """
        with self.request_lock:
            ResumableUploadHandler.request_counter += 1
            req_id = ResumableUploadHandler.request_counter

        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n{'='*60}")
        print(f"[{timestamp}] 🌐 GET #{req_id} - Path: {self.path}")
        print(
            f"[{timestamp}] 📍 Client: {self.client_address[0]}:{self.client_address[1]}"
        )
        print(f"[{timestamp}] 🔧 User-Agent: {self.headers.get('User-Agent', 'N/A')}")
        print(f"{'='*60}")

        # Remove GET parameters from URL for comparison
        clean_path = self.path.split("?")[0]

        if clean_path == "/":
            print(f"[{timestamp}] ✅ Serving upload page...")
            self.serve_upload_page()
            print(f"[{timestamp}] ✅ Page sent successfully!")
        elif clean_path == "/files":
            print(f"[{timestamp}] 📂 Listing directory files...")
            self.serve_list_files()
            print(f"[{timestamp}] ✅ File list sent!")
        elif clean_path.startswith("/download/"):
            _, _, filename = clean_path.partition("/download/")
            print(f"[{timestamp}] 📥 Starting download: {filename}")
            self.serve_download_file(filename)
        elif clean_path.startswith("/status/"):
            pass  # Status checks
        else:
            print(f"[{timestamp}] ❌ Path not found: {self.path}")
            self.send_error(404)

    def do_POST(self):
        """
        Handle POST requests for file uploads.
        """
        with self.request_lock:
            ResumableUploadHandler.request_counter += 1
            req_id = ResumableUploadHandler.request_counter

        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n{'='*60}")
        print(f"[{timestamp}] 📥 POST #{req_id} - Path: {self.path}")
        print(
            f"[{timestamp}] 📍 Client: {self.client_address[0]}:{self.client_address[1]}"
        )
        print(
            f"[{timestamp}] 📦 Content-Length: "
            f"{self.headers.get('Content-Length', 'N/A')} bytes"
        )
        print(
            f"[{timestamp}] 🔧 Content-Type: "
            f"{self.headers.get('Content-Type', 'N/A')[:50]}..."
        )
        print(f"{'='*60}")

        if self.path == "/upload":
            print(f"[{timestamp}] ✅ Processing upload...")
            self.handle_chunk_upload()
        else:
            print(f"[{timestamp}] ❌ Path not found: {self.path}")
            self.send_error(404)

    def serve_upload_page(self):
        """
        Serve the upload web interface.
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

        html = get_upload_page_html()
        self.wfile.write(html.encode())

    def serve_list_files(self):
        """
        Serve JSON list of files in the upload directory.
        """
        try:
            files = []
            if os.path.exists(self.upload_dir):
                for fname in os.listdir(self.upload_dir):
                    fpath = os.path.join(self.upload_dir, fname)
                    if os.path.isfile(fpath):
                        size = os.path.getsize(fpath)
                        mtime = os.path.getmtime(fpath)
                        files.append(
                            {
                                "name": fname,
                                "size": size,
                                "modified": datetime.fromtimestamp(mtime).strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            }
                        )

            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] 📋 Found {len(files)} files in directory")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(files).encode())

        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] ❌ Error listing files: {str(e)}")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def serve_download_file(self, filename):
        """
        Serve file download.

        Args:
            filename (str): Name of the file to download
        """
        safe_name = sanitize_filename(filename)
        file_path = os.path.join(self.upload_dir, safe_name)

        if not os.path.isfile(file_path):
            self.send_error(404, "File not found")
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Disposition", f'attachment; filename="{safe_name}"')
        self.send_header("Content-Length", str(os.path.getsize(file_path)))
        self.end_headers()

        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                self.wfile.write(chunk)

    def handle_chunk_upload(self):
        """
        Handle chunked file upload with resume capability.
        """
        start_time = time.time()
        timestamp = datetime.now().strftime("%H:%M:%S")

        try:
            print(f"[{timestamp}] 🔍 Starting data parsing...")

            content_type = self.headers["Content-Type"]
            if "multipart/form-data" not in content_type:
                raise Exception("Invalid content type")

            content_length = int(self.headers["Content-Length"])
            payload_kb = content_length / 1024
            print(f"[{timestamp}] 📊 Payload size: {payload_kb:.2f} KB")

            boundary = content_type.split("boundary=")[1].encode()
            print(f"[{timestamp}] 📥 Reading client data...")

            data = self.rfile.read(content_length)
            print(f"[{timestamp}] ✅ Data read: {len(data)} bytes")

            parts = data.split(b"--" + boundary)
            chunk_data = None
            filename = None
            chunk_index = None
            total_chunks = None

            print(f"[{timestamp}] 🔍 Extracting form fields...")

            # Extract form fields
            for part in parts:
                if b'name="chunk"' in part:
                    chunk_data = part.split(b"\r\n\r\n", 1)[1].rsplit(b"\r\n", 1)[0]
                elif b'name="filename"' in part:
                    filename = (
                        part.split(b"\r\n\r\n", 1)[1].rsplit(b"\r\n", 1)[0].decode()
                    )
                    filename = sanitize_filename(filename)
                elif b'name="chunkIndex"' in part:
                    chunk_index = int(
                        part.split(b"\r\n\r\n", 1)[1].rsplit(b"\r\n", 1)[0]
                    )
                elif b'name="totalChunks"' in part:
                    total_chunks = int(
                        part.split(b"\r\n\r\n", 1)[1].rsplit(b"\r\n", 1)[0]
                    )
                elif b'name="fileSize"' in part:
                    # File size extracted but not used
                    _ = int(
                        part.split(b"\r\n\r\n", 1)[1].rsplit(b"\r\n", 1)[0]
                    )  # noqa: F841

            if (
                not chunk_data
                or filename is None
                or chunk_index is None
                or total_chunks is None
            ):
                raise Exception("Missing required data")

            chunk_kb = len(chunk_data) / 1024
            print(f"[{timestamp}] ✅ Fields extracted:")
            print(f"[{timestamp}]    - File: {filename}")
            print(f"[{timestamp}]    - Chunk: {chunk_index + 1}/{total_chunks}")
            print(f"[{timestamp}]    - Chunk size: {chunk_kb:.2f} KB")

            # Ensure temp directory exists
            os.makedirs(self.temp_dir, exist_ok=True)
            temp_file = os.path.join(self.temp_dir, f"{filename}.part")

            # Append to existing file or create new one
            mode = "ab" if chunk_index > 0 else "wb"
            print(f"[{timestamp}] 💾 Saving chunk to disk (mode: {mode})...")

            with open(temp_file, mode) as f:
                f.write(chunk_data)

            current_size = os.path.getsize(temp_file)
            percent = int((chunk_index + 1) / total_chunks * 100)
            current_mb = current_size / 1024 / 1024
            print(
                f"[{timestamp}] ✅ Chunk saved! Accumulated size: {current_mb:.2f} MB"
            )

            # Log progress for every 100 chunks or final chunk
            if (chunk_index + 1) % 100 == 0 or chunk_index + 1 >= total_chunks:
                print(f"\n{'='*60}")
                print(
                    f"[{timestamp}] 📊 PROGRESS: "
                    f"{chunk_index + 1}/{total_chunks} ({percent}%)"
                )
                print(f"[{timestamp}] 📦 Current size: {current_mb:.2f} MB")
                print(f"{'='*60}\n")

            # Move to final location when complete
            if chunk_index + 1 >= total_chunks:
                print(f"[{timestamp}] 🎉 LAST CHUNK RECEIVED!")
                final_path = os.path.join(self.upload_dir, filename)
                print(f"[{timestamp}] 📁 Moving to: {final_path}")

                os.rename(temp_file, final_path)
                final_size = os.path.getsize(final_path)
                size_gb = final_size / 1024 / 1024 / 1024

                print(f"\n{'='*70}")
                print("✅✅✅ FILE COMPLETELY RECEIVED SUCCESSFULLY! ✅✅✅")
                print(f"{'='*70}")
                print(f"📁 File: {final_path}")
                print(f"📦 Size: {size_gb:.2f} GB ({final_size:,} bytes)")
                print(
                    f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                print(f"{'='*70}\n")

            processing_time = time.time() - start_time
            print(f"[{timestamp}] ⚡ Processing time: {processing_time:.3f}s")

            # Send response
            response = {
                "success": True,
                "chunkIndex": chunk_index,
                "received": current_size,
                "complete": chunk_index + 1 >= total_chunks,
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

            print(f"[{timestamp}] ✅ JSON response sent to client")

        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"\n{'='*60}")
            print(f"[{timestamp}] ❌❌❌ UPLOAD ERROR ❌❌❌")
            print(f"[{timestamp}] Message: {e}")
            print(f"{'='*60}")

            import traceback

            traceback.print_exc()

            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
