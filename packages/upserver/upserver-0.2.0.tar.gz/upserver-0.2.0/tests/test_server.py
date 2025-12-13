"""
Tests for the FileServer class.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from upserver.server import FileServer


class TestFileServer:
    """Test cases for FileServer class."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)

    def test_initialization(self, temp_dir):
        """Test FileServer initialization."""
        server = FileServer(upload_dir=temp_dir, host="127.0.0.1", port=9000)
        assert server.host == "127.0.0.1"
        assert server.port == 9000
        assert server.upload_dir == Path(temp_dir)
        assert server.upload_dir.exists()

    def test_upload_file(self, temp_dir):
        """Test file upload functionality."""
        server = FileServer(upload_dir=temp_dir)
        test_data = b"Hello, World!"
        filename = "test.txt"

        result = server.upload_file(test_data, filename)

        assert result.exists()
        assert result.name == filename
        with open(result, "rb") as f:
            assert f.read() == test_data

    def test_download_file(self, temp_dir):
        """Test file download functionality."""
        server = FileServer(upload_dir=temp_dir)
        test_data = b"Test content"
        filename = "download_test.txt"

        # Upload a file first
        server.upload_file(test_data, filename)

        # Download it
        downloaded_data = server.download_file(filename)
        assert downloaded_data == test_data

    def test_download_nonexistent_file(self, temp_dir):
        """Test downloading a file that doesn't exist."""
        server = FileServer(upload_dir=temp_dir)

        with pytest.raises(FileNotFoundError):
            server.download_file("nonexistent.txt")

    def test_list_files(self, temp_dir):
        """Test listing files in upload directory."""
        server = FileServer(upload_dir=temp_dir)

        # Initially empty
        assert server.list_files() == []

        # Upload some files
        server.upload_file(b"data1", "file1.txt")
        server.upload_file(b"data2", "file2.txt")

        files = server.list_files()
        assert len(files) == 2
        assert "file1.txt" in files
        assert "file2.txt" in files

    def test_upload_directory_creation(self):
        """Test that upload directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            upload_path = Path(temp_dir) / "new_uploads"
            assert not upload_path.exists()

            # server = FileServer(upload_dir=str(upload_path))
            FileServer(upload_dir=str(upload_path))  # noqa: F841
            assert upload_path.exists()

    def test_path_traversal_protection_upload(self, temp_dir):
        """Test that path traversal attacks are prevented in upload."""
        server = FileServer(upload_dir=temp_dir)
        test_data = b"malicious content"

        # Try to upload with path traversal
        result = server.upload_file(test_data, "../../../malicious.txt")

        # File should be saved in the upload directory, not outside
        assert result.parent == Path(temp_dir)
        assert result.name == "malicious.txt"

    def test_path_traversal_protection_download(self, temp_dir):
        """Test that path traversal attacks are prevented in download."""
        server = FileServer(upload_dir=temp_dir)
        test_data = b"safe content"

        # Upload a legitimate file
        server.upload_file(test_data, "safe.txt")

        # Try to download with path traversal
        # Should look for "etc/passwd" as a filename, not as a path
        with pytest.raises(FileNotFoundError):
            server.download_file("../../../etc/passwd")
