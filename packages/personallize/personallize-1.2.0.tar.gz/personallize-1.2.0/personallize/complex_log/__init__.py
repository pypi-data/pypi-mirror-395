"""
Complex logging module for personallize.
Provides advanced logging capabilities with configuration management.

Usage Examples:

    Basic Usage with LogManager:
        >>> from personallize.complex_log import LogManager, LogConfig
        >>> manager = LogManager()
        >>> logger, exception_decorator = manager.get_logger()
        >>> logger.info("Hello World!")

    Using LogConfig for custom configuration:
        >>> from personallize.complex_log import LogManager, LogConfig
        >>> config = LogConfig.simple()  # Simple console-only logging
        >>> manager = LogManager(config)
        >>> logger, decorator = manager.get_simple_logger("my_app")
        >>> logger.info("Application started")

    File logging with custom configuration:
        >>> config = LogConfig.file_only(level="DEBUG", log_dir="my_logs")
        >>> manager = LogManager(config)
        >>> logger, decorator = manager.get_simple_logger("debug_app", "debug.log")
        >>> logger.debug("Debug information")

    Advanced configuration:
        >>> config = LogConfig(
        ...     level="INFO",
        ...     log_dir="logs",
        ...     console_enabled=True,
        ...     file_enabled=True,
        ...     json_format=False,
        ...     colored_console=True
        ... )
        >>> manager = LogManager(config)
        >>> logger, decorator = manager.get_simple_logger("advanced_app")

    Using exception decorator:
        >>> manager = LogManager()
        >>> logger, exception_decorator = manager.get_logger()
        >>> @exception_decorator
        ... def my_function():
        ...     raise ValueError("Something went wrong")
        >>> my_function()  # Exception will be logged automatically

Available LogConfig presets:
    - LogConfig.simple(): Console-only logging with basic formatting
    - LogConfig.file_only(): File-only logging with JSON format
    - LogConfig(): Full-featured logging with both console and file output

Configuration Options:
    - level: Logging level ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    - log_dir: Directory for log files (default: "logs")
    - console_enabled: Enable console output (default: True)
    - file_enabled: Enable file output (default: True)
    - json_format: Use JSON formatting for logs (default: True)
    - colored_console: Enable colored console output (default: True)
    - max_file_size: Maximum log file size in MB (default: 10)
    - backup_count: Number of backup files to keep (default: 5)
    - queue_enabled: Enable asynchronous logging (default: True)
    - rich_handler: Use Rich handler for enhanced console output (default: True)
"""

from .config import LogConfig
from .manager import LogManager

__all__ = ["LogConfig", "LogManager"]
