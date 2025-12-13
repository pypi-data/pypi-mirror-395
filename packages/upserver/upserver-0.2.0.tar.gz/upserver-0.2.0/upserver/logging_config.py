"""
Logging configuration for the upserver package.
"""

import logging
import sys

from pathlib import Path
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter with colors for different log levels.
    """

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        """
        Format log record with colors.
        """
        # Add color to levelname
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}" f"{record.levelname}" f"{self.RESET}"
            )

        return super().format(record)


def setup_logging(
    enable_logging: bool = True,
    log_file: Optional[str] = None,
    log_level: str = "INFO",
    enable_colors: bool = True,
) -> logging.Logger:
    """
    Set up logging configuration for the server.

    Args:
        enable_logging (bool): Enable logging
        log_file (Optional[str]): Path to log file (None = stdout only)
        log_level (str): Logging level
        enable_colors (bool): Enable colored output for console

    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger("upserver")

    # Clear existing handlers
    logger.handlers.clear()

    if not enable_logging:
        logger.disabled = True
        return logger

    # Set log level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    # Create formatters
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - "
        "%(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    simple_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s", datefmt="%H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    if enable_colors and hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
        console_formatter = ColoredFormatter(
            "[%(asctime)s] %(levelname)s: %(message)s", datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_formatter)
    else:
        console_handler.setFormatter(simple_formatter)

    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)

    return logger


class ServerLogger:
    """
    Logger wrapper with server-specific functionality.
    """

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.request_counter = 0

    def log_request(
        self,
        method: str,
        path: str,
        client_address: tuple,
        user_agent: Optional[str] = None,
    ):
        """
        Log HTTP request details.
        """
        self.request_counter += 1
        client_ip = client_address[0] if client_address else "unknown"

        msg = f"{method} #{self.request_counter} - {path} from {client_ip}"
        if user_agent:
            msg += (
                f" ({user_agent[:50]}...)"
                if len(user_agent) > 50
                else f" ({user_agent})"
            )

        self.logger.info(msg)

    def log_upload_progress(
        self,
        filename: str,
        chunk_index: int,
        total_chunks: int,
        current_size: int,
        processing_time: float,
    ):
        """
        Log upload progress.
        """
        percent = int((chunk_index + 1) / total_chunks * 100)
        size_mb = current_size / 1024 / 1024

        self.logger.info(
            f"Upload progress: {filename} - Chunk {chunk_index + 1}/{total_chunks} "
            f"({percent}%) - {size_mb:.2f} MB - {processing_time:.3f}s"
        )

    def log_upload_complete(self, filename: str, final_size: int, total_time: float):
        """
        Log upload completion.
        """
        size_mb = final_size / 1024 / 1024
        speed_mbps = size_mb / total_time if total_time > 0 else 0

        self.logger.info(
            f"Upload completed: {filename} - {size_mb:.2f} MB in {total_time:.2f}s "
            f"(avg {speed_mbps:.2f} MB/s)"
        )

    def log_error(self, message: str, exception: Optional[Exception] = None):
        """
        Log error with optional exception details.
        """
        if exception:
            self.logger.error(f"{message}: {str(exception)}", exc_info=True)
        else:
            self.logger.error(message)

    def log_startup(self, config_info: dict):
        """
        Log server startup information.
        """
        self.logger.info("=" * 50)
        self.logger.info("UPSERVER STARTING UP")
        self.logger.info("=" * 50)

        for key, value in config_info.items():
            self.logger.info(f"{key}: {value}")

        self.logger.info("=" * 50)
        self.logger.info("Server ready to accept connections")

    def log_shutdown(self):
        """
        Log server shutdown.
        """
        self.logger.info("Server shutting down gracefully")

    # Delegate other logging methods
    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)
