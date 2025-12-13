# upserver

A resumable HTTP file server for uploading and downloading files with web interface.

## Description

`upserver` is a robust and efficient file server package that provides resumable chunked file uploads, web-based file management, and real-time progress tracking. It's designed to handle large files reliably with automatic resume capability and cross-platform compatibility.

## ✨ Features

- **🔄 Resumable Uploads**: Automatic chunked uploads with resume capability
- **🌐 Web Interface**: Beautiful, responsive web UI for file management
- **📊 Real-time Progress**: Live upload progress with speed and time estimates
- **⏸️ Pause/Resume**: Manual pause and resume control for uploads
- **📱 Cross-platform**: Works on Windows, Linux, and macOS
- **🛡️ Security**: Filename sanitization and path traversal protection
- **⚙️ Configurable**: Flexible configuration via CLI, files, or environment variables
- **📝 Logging**: Comprehensive logging with file and console output
- **📦 Any File Type**: Supports unlimited file types and sizes
- **🚀 High Performance**: Optimized for large file transfers

## Installation

You can install `upserver` using pip:

```bash
pip install upserver
```

Or install from source:

```bash
git clone https://github.com/eiAlex/upserver.git
cd upserver
pip install -e .
```

## Usage

### Quick Start

Start the server with default settings:

```bash
upserver
```

The server will start on `http://localhost:8000` with a web interface for file uploads and management.

### Command-Line Options

```bash
upserver --host 127.0.0.1 --port 8080 --upload-dir /path/to/uploads
```

#### Server Configuration
- `--host`: Host address to bind the server (default: 0.0.0.0)
- `--port`: Port number to bind the server (default: 8000)  
- `--upload-dir`: Directory to store uploaded files (default: uploads)
- `--chunk-size`: Size of upload chunks in bytes (default: 5MB)
- `--max-file-size`: Maximum file size allowed in bytes (0 = unlimited)

#### Configuration Management
- `--config`: Load configuration from JSON file
- `--save-config`: Save current configuration to JSON file and exit

#### Logging Options
- `--log-file`: Path to log file (default: stdout only)
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `--no-colors`: Disable colored output
- `--quiet`: Disable all logging output

#### Other Options
- `--version`: Show the version number
- `--help`: Show help message with all options

### Configuration File

Create a configuration file for persistent settings:

```bash
upserver --save-config config.json
```

Example configuration file:
```json
{
    "host": "0.0.0.0",
    "port": 8080,
    "upload_dir": "/var/uploads", 
    "chunk_size": 10485760,
    "max_file_size": 0,
    "enable_logging": true,
    "log_file": "upserver.log",
    "cors_enabled": true,
    "allowed_origins": ["*"]
}
```

Load configuration:
```bash
upserver --config config.json
```

### Environment Variables

Configure via environment variables:
- `UPSERVER_HOST`: Server host address
- `UPSERVER_PORT`: Server port number
- `UPSERVER_UPLOAD_DIR`: Upload directory path
- `UPSERVER_CHUNK_SIZE`: Upload chunk size in bytes
- `UPSERVER_MAX_FILE_SIZE`: Maximum file size in bytes
- `UPSERVER_ENABLE_LOGGING`: Enable logging (true/false)
- `UPSERVER_LOG_FILE`: Log file path
- `UPSERVER_CORS_ENABLED`: Enable CORS (true/false)

### As a Python Module

Use `upserver` programmatically in your Python applications:

```python
from upserver import FileServer, ServerConfig

# Basic usage
server = FileServer(
    upload_dir="my_uploads",
    host="127.0.0.1", 
    port=8080,
    chunk_size=10*1024*1024  # 10MB chunks
)

# Start the server (blocks until stopped)
server.start()
```

#### Advanced Configuration

```python
from upserver import FileServer, ServerConfig, setup_logging, ServerLogger

# Create configuration
config = ServerConfig(
    host="0.0.0.0",
    port=8000,
    upload_dir="uploads",
    chunk_size=5*1024*1024,  # 5MB
    max_file_size=0,  # Unlimited
    enable_logging=True,
    log_file="server.log"
)

# Setup logging
logger = setup_logging(
    enable_logging=config.enable_logging,
    log_file=config.log_file,
    log_level="INFO"
)

server_logger = ServerLogger(logger)

# Create and start server  
server = FileServer(
    upload_dir=config.upload_dir,
    host=config.host,
    port=config.port,
    chunk_size=config.chunk_size
)

try:
    server_logger.info("Starting upserver")
    server.start()
except KeyboardInterrupt:
    server_logger.info("Server stopped by user")
    server.stop()
```

#### File Operations

The legacy simple file operations are still available:

```python
from upserver.utils import sanitize_filename, get_disk_space, format_file_size

# Utility functions
safe_name = sanitize_filename("../../../etc/passwd")  # Returns "passwd"
total, used, free = get_disk_space("/")
size_str = format_file_size(1024*1024*1024)  # Returns "1.00 GB"
```

### Running as a Module

You can also run upserver as a Python module:

```bash
python -m upserver
```

## 🚀 Web Interface

Access the web interface at `http://localhost:8000` (or your configured address) to:

- **📤 Upload Files**: Drag & drop or select files with resume capability
- **📋 List Files**: View all uploaded files with details
- **📥 Download Files**: Direct download links for all files  
- **📊 Progress Tracking**: Real-time upload progress with speed metrics
- **⏸️ Upload Control**: Pause and resume uploads as needed

## 🔧 API Endpoints

The server provides RESTful endpoints:

- `GET /`: Web interface for file management
- `GET /files`: JSON list of uploaded files
- `GET /download/{filename}`: Download specific file
- `POST /upload`: Chunked file upload endpoint (multipart/form-data)

## 📊 Upload Protocol

The resumable upload system uses chunked transfers:

1. **File Selection**: Client selects file for upload
2. **Chunking**: File is split into configurable chunks (default: 5MB)
3. **Sequential Upload**: Chunks are uploaded sequentially with progress tracking
4. **Resume Capability**: Failed uploads automatically resume from last successful chunk
5. **Assembly**: Server assembles chunks into final file when complete

### Upload Request Format

```javascript
// Each chunk is sent as multipart/form-data with:
{
    chunk: Blob,           // File chunk data
    filename: String,      // Original filename
    chunkIndex: Number,    // Current chunk index (0-based)
    totalChunks: Number,   // Total number of chunks
    fileSize: Number       // Total file size in bytes
}
```

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/eiAlex/upserver.git
cd upserver

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black upserver/
```

### Type Checking

```bash
mypy upserver/
```

## 📋 Requirements

- Python >= 3.8
- No external dependencies (uses only Python standard library)

## 🔒 Security Features

- **Filename Sanitization**: Automatic cleanup of unsafe filenames
- **Path Traversal Protection**: Prevents directory traversal attacks
- **CORS Support**: Configurable cross-origin resource sharing
- **File Type Validation**: Optional file type restrictions
- **Size Limits**: Configurable maximum file size limits

## 🌟 Use Cases

- **Large File Transfers**: Reliable transfer of GB+ files
- **Backup Solutions**: Automated backup uploads with resume capability
- **Content Management**: Web-based file management system
- **Development Testing**: Quick file server for development environments
- **Media Distribution**: Sharing large media files with progress tracking

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Álex Vieira

## 🤝 Contributing

We welcome contributions from the community! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Setting up development environment
- Code style guidelines  
- Testing procedures
- Submitting pull requests
- Reporting bugs and feature requests

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/upserver.git
cd upserver

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy build twine
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=upserver --cov-report=term-missing

# Run specific test
python -m pytest tests/test_server.py::TestFileServer::test_start_stop -v
```

### Code Quality

```bash
# Format code
python -m black upserver/ tests/

# Check linting
python -m flake8 upserver/ tests/ --max-line-length=88

# Type checking
python -m mypy upserver/ --ignore-missing-imports
```

### Building and Publishing

```bash
# Use the build script
python build.py full

# Or manual steps:
python build.py clean
python build.py test
python build.py build
python build.py check

# Upload to Test PyPI
python build.py upload-test

# Upload to PyPI (production)
python build.py upload
```

### Quick Start for Contributors

```bash
# Clone the repository
git clone https://github.com/eiAlex/upserver.git
cd upserver

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run code quality checks
black upserver/
flake8 upserver/
mypy upserver/
```

## 🛠️ Troubleshooting

### Common Issues

1. **Port already in use**: Change port with `--port 8080`
2. **Permission denied**: Ensure write permissions to upload directory
3. **Large file uploads fail**: Increase chunk size with `--chunk-size`
4. **Memory issues**: Reduce chunk size for low-memory systems

### Debug Mode

Enable debug logging for troubleshooting:

```bash
upserver --log-level DEBUG --log-file debug.log
```

### Performance Tuning

For optimal performance:
- Use SSD storage for upload directory
- Adjust chunk size based on network conditions
- Configure appropriate file size limits
- Monitor system resources during large transfers

## 🛠️ Development

### Setting Up Development Environment

1. **Clone the repository:**
```bash
git clone https://github.com/eiAlex/upserver.git
cd upserver
```

2. **Create and activate virtual environment:**
```bash
python -m venv .venv

# Windows
source .venv/Scripts/activate

# Linux/macOS  
source .venv/bin/activate
```

3. **Install development dependencies:**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Code Quality Tools

This project uses several tools to maintain code quality:

#### 🎨 Code Formatting
```bash
# Format all Python files
black .

# Check formatting without making changes
black --check .
```

#### 🔍 Linting
```bash
# Run flake8 linter
flake8

# Fix specific issues manually based on output
```

#### 🏷️ Type Checking
```bash
# Run mypy type checker
mypy upserver/

# Check specific files
mypy upserver/server.py
```

#### 🔒 Security Analysis
```bash
# Run bandit security linter
bandit -r upserver -c .bandit

# Check for known vulnerabilities
safety scan
```

#### 🧪 Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=upserver

# Run specific test file
pytest tests/test_server.py
```

### Pre-commit Quality Checks

Before pushing code, run all quality checks:

```bash
# Quick quality check script
python scripts/build_helper.py quality

# Or run individual tools:
black --check .
flake8
mypy upserver
bandit -r upserver -c .bandit
safety scan
pytest
```

### Build and Package

```bash
# Clean previous builds
python scripts/build_helper.py clean

# Build package
python scripts/build_helper.py build
# or
python -m build

# The built packages will be in dist/
```

### Development Workflow

1. **Create feature branch**: `git checkout -b feature/your-feature`
2. **Make changes** with proper code formatting and type hints
3. **Run quality checks**: `python scripts/build_helper.py quality`
4. **Run tests**: `pytest`
5. **Commit changes**: `git commit -m "feat: description"`
6. **Push and create PR**: `git push origin feature/your-feature`

### CI/CD Pipeline

The project uses GitHub Actions for automated:

- **✅ Testing**: Multi-platform testing (Windows, Linux, macOS)
- **🔍 Code Quality**: Black, flake8, mypy checks
- **🔒 Security**: Bandit and Safety scans
- **📦 Building**: Automated package building
- **🚀 Publishing**: Automatic PyPI publishing on main branch

### Configuration Files

- **`.flake8`**: Linting configuration with specific ignores
- **`.bandit`**: Security scanner configuration  
- **`pyproject.toml`**: Project metadata and mypy settings
- **`requirements-dev.txt`**: Development dependencies
- **`.github/workflows/ci.yml`**: CI/CD pipeline definition

### Helper Scripts

The `scripts/build_helper.py` provides convenient commands:

```bash
python scripts/build_helper.py clean    # Clean build artifacts
python scripts/build_helper.py deps     # Install dependencies  
python scripts/build_helper.py test     # Run tests
python scripts/build_helper.py quality  # Run all quality checks
python scripts/build_helper.py build    # Build package
```

## Support

If you encounter any problems or have suggestions, please open an issue on the [GitHub repository](https://github.com/eiAlex/upserver/issues).