"""
Configuration management for the upserver package.
"""

import os
import json
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import Optional


@dataclass
class ServerConfig:
    """
    Configuration class for the file server.

    Attributes:
        host (str): Server host address
        port (int): Server port number
        upload_dir (str): Directory to store uploaded files
        chunk_size (int): Size of upload chunks in bytes
        max_file_size (int): Maximum file size allowed (0 = unlimited)
        enable_logging (bool): Enable detailed logging
        log_file (Optional[str]): Path to log file (None = stdout only)
        cors_enabled (bool): Enable CORS headers
        allowed_origins (list): List of allowed origins for CORS
    """

    host: str = "0.0.0.0"  # nosec B104 - intentional binding for file server
    port: int = 8000
    upload_dir: str = "uploads"
    chunk_size: int = 5 * 1024 * 1024  # 5MB
    max_file_size: int = 0  # 0 = unlimited
    enable_logging: bool = True
    log_file: Optional[str] = None
    cors_enabled: bool = True
    allowed_origins: list = field(default_factory=list)

    def __post_init__(self):
        """
        Post-initialization to set default values.
        """
        if self.allowed_origins is None:
            self.allowed_origins = ["*"]

    @classmethod
    def load_from_file(cls, config_path: str) -> "ServerConfig":
        """
        Load configuration from a JSON file.

        Args:
            config_path (str): Path to the configuration file

        Returns:
            ServerConfig: Loaded configuration
        """
        config_file = Path(config_path)
        if not config_file.exists():
            return cls()

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config_data = json.load(f)
            return cls(**config_data)
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Warning: Error loading config from {config_path}: {e}")
            print("Using default configuration.")
            return cls()

    def save_to_file(self, config_path: str):
        """
        Save configuration to a JSON file.

        Args:
            config_path (str): Path to save the configuration file
        """
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)

        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=4)

    @classmethod
    def from_env(cls) -> "ServerConfig":
        """
        Create configuration from environment variables.

        Returns:
            ServerConfig: Configuration with values from environment
        """
        return cls(
            host=os.getenv("UPSERVER_HOST", "0.0.0.0"),  # nosec B104
            port=int(os.getenv("UPSERVER_PORT", "8000")),
            upload_dir=os.getenv("UPSERVER_UPLOAD_DIR", "uploads"),
            chunk_size=int(os.getenv("UPSERVER_CHUNK_SIZE", str(5 * 1024 * 1024))),
            max_file_size=int(os.getenv("UPSERVER_MAX_FILE_SIZE", "0")),
            enable_logging=os.getenv("UPSERVER_ENABLE_LOGGING", "true").lower()
            == "true",
            log_file=os.getenv("UPSERVER_LOG_FILE"),
            cors_enabled=os.getenv("UPSERVER_CORS_ENABLED", "true").lower() == "true",
        )

    def update_from_args(self, args):
        """
        Update configuration from command line arguments.

        Args:
            args: Parsed command line arguments
        """
        if hasattr(args, "host") and args.host:
            self.host = args.host
        if hasattr(args, "port") and args.port:
            self.port = args.port
        if hasattr(args, "upload_dir") and args.upload_dir:
            self.upload_dir = args.upload_dir
        if hasattr(args, "chunk_size") and args.chunk_size:
            self.chunk_size = args.chunk_size
        if hasattr(args, "max_file_size") and args.max_file_size:
            self.max_file_size = args.max_file_size
        if hasattr(args, "log_file") and args.log_file:
            self.log_file = args.log_file

    def validate(self) -> bool:
        """
        Validate the configuration.

        Returns:
            bool: True if configuration is valid
        """
        if not isinstance(self.port, int) or self.port < 1 or self.port > 65535:
            print(f"Error: Invalid port number: {self.port}")
            return False

        if self.chunk_size < 1024:  # Minimum 1KB
            print(f"Error: Chunk size too small: {self.chunk_size}")
            return False

        if self.max_file_size < 0:
            print(f"Error: Invalid max file size: {self.max_file_size}")
            return False

        return True
