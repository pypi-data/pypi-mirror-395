"""
Command-line interface for the upserver package.
"""

import argparse
import sys


from .server import FileServer
from .config import ServerConfig
from .logging_config import setup_logging, ServerLogger
from . import __version__


def create_parser():
    """
    Create and configure argument parser.

    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description=(
            "upserver - A resumable file server for uploading and downloading files"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Start with default settings
  %(prog)s --host 127.0.0.1 --port 8080      # Custom host and port
  %(prog)s --upload-dir /path/to/uploads      # Custom upload directory
  %(prog)s --config config.json              # Load from config file
  %(prog)s --chunk-size 10485760              # Use 10MB chunks
  %(prog)s --log-file server.log              # Log to file

Configuration priority: CLI arguments > config file > environment variables > defaults
        """,
    )

    parser.add_argument(
        "--version", action="version", version=f"upserver {__version__}"
    )

    # Server configuration
    server_group = parser.add_argument_group("Server Configuration")
    server_group.add_argument(
        "--host", type=str, help="Host address to bind the server (default: 0.0.0.0)"
    )

    server_group.add_argument(
        "--port", type=int, help="Port number to bind the server (default: 8000)"
    )

    server_group.add_argument(
        "--upload-dir",
        type=str,
        help="Directory to store uploaded files (default: uploads)",
    )

    server_group.add_argument(
        "--chunk-size", type=int, help="Size of upload chunks in bytes (default: 5MB)"
    )

    server_group.add_argument(
        "--max-file-size",
        type=int,
        help="Maximum file size allowed in bytes (0 = unlimited, default: 0)",
    )

    # Configuration file
    config_group = parser.add_argument_group("Configuration")
    config_group.add_argument(
        "--config", type=str, help="Load configuration from JSON file"
    )

    config_group.add_argument(
        "--save-config",
        type=str,
        help="Save current configuration to JSON file and exit",
    )

    # Logging configuration
    logging_group = parser.add_argument_group("Logging")
    logging_group.add_argument(
        "--log-file", type=str, help="Path to log file (default: stdout only)"
    )

    logging_group.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)",
    )

    logging_group.add_argument(
        "--no-colors", action="store_true", help="Disable colored output"
    )

    logging_group.add_argument(
        "--quiet", action="store_true", help="Disable all logging output"
    )

    return parser


def main():
    """
    Main CLI entry point for upserver.
    """
    parser = create_parser()
    args = parser.parse_args()

    try:
        # Load configuration
        if args.config:
            config = ServerConfig.load_from_file(args.config)
        else:
            # Start with environment variables, then apply CLI args
            config = ServerConfig.from_env()

        # Update configuration with CLI arguments
        config.update_from_args(args)

        # Handle save-config option
        if args.save_config:
            config.save_to_file(args.save_config)
            print(f"Configuration saved to: {args.save_config}")
            return

        # Validate configuration
        if not config.validate():
            sys.exit(1)

        # Setup logging
        enable_logging = not args.quiet
        log_level = args.log_level if not args.quiet else "CRITICAL"
        enable_colors = not args.no_colors

        logger_instance = setup_logging(
            enable_logging=enable_logging,
            log_file=config.log_file,
            log_level=log_level,
            enable_colors=enable_colors,
        )

        server_logger = ServerLogger(logger_instance)

        # Create and start server
        server = FileServer(
            upload_dir=config.upload_dir,
            host=config.host,
            port=config.port,
            chunk_size=config.chunk_size,
        )

        # Log startup information
        if enable_logging:
            config_info = {
                "Host": config.host,
                "Port": config.port,
                "Upload Directory": config.upload_dir,
                "Chunk Size": f"{config.chunk_size / (1024*1024):.1f} MB",
                "Max File Size": (
                    "Unlimited"
                    if config.max_file_size == 0
                    else f"{config.max_file_size} bytes"
                ),
                "Log File": config.log_file or "Console only",
                "Version": __version__,
            }
            server_logger.log_startup(config_info)

        server.start()

    except KeyboardInterrupt:
        if "server_logger" in locals():
            server_logger.log_shutdown()
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        if "server_logger" in locals():
            server_logger.log_error("Server startup failed", e)
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
