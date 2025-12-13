"""
Configuration management for complex logging.

This module provides the LogConfig class for managing logging configurations
with various presets and customization options.

Usage Examples:

    Simple console-only logging:
        >>> config = LogConfig.simple()
        >>> print(config.console_enabled)  # True
        >>> print(config.file_enabled)    # False

    File-only logging with custom directory:
        >>> config = LogConfig.file_only(level="DEBUG", log_dir="debug_logs")
        >>> print(config.level)           # DEBUG
        >>> print(config.log_dir)         # debug_logs

    Full-featured logging:
        >>> config = LogConfig(
        ...     level="INFO",
        ...     log_dir="application_logs",
        ...     json_format=False,
        ...     colored_console=True
        ... )
        >>> print(config.json_format)     # False
        >>> print(config.colored_console) # True

    Custom configuration with all options:
        >>> config = LogConfig(
        ...     level="WARNING",
        ...     log_dir="custom_logs",
        ...     console_enabled=True,
        ...     file_enabled=True,
        ...     json_format=True,
        ...     colored_console=False,
        ...     max_file_size=20,
        ...     backup_count=10,
        ...     queue_enabled=False,
        ...     rich_handler=False
        ... )

Available Presets:
    - LogConfig.simple(): Minimal console-only logging
    - LogConfig.file_only(): File-only logging with JSON format
    - LogConfig(): Default full-featured configuration
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

type LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


@dataclass
class LogConfig:
    """
    Logging configuration container for complex_log.

    Attributes:
        level: Default logging level
        log_dir: Directory where log files will be stored
        console_enabled: Enable console logging
        file_enabled: Enable file logging
        json_format: Use JSON formatting for logs
        colored_console: Enable colored console output
        max_file_size: Maximum size for log files (in MB)
        backup_count: Number of backup files to keep
        queue_enabled: Enable asynchronous logging with queue
        rich_handler: Use Rich handler for enhanced console output
        propagate: Whether loggers should propagate to parent loggers
        format_string: Custom format string for logging
        date_format: Date format for timestamps
        custom_formatters: Custom formatter configurations
        custom_handlers: Custom handler configurations
        custom_filters: Custom filter configurations
    """

    level: LogLevel = "INFO"
    log_dir: str = "logs"
    console_enabled: bool = True
    file_enabled: bool = True
    json_format: bool = True
    colored_console: bool = True
    max_file_size: int = 10  # MB
    backup_count: int = 5
    queue_enabled: bool = True
    rich_handler: bool = True
    propagate: bool = True
    format_string: str = "[%(asctime)s] %(levelname_icon)s %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    custom_formatters: dict[str, Any] | None = None
    custom_handlers: dict[str, Any] | None = None
    custom_filters: dict[str, Any] | None = None
    # Configurações de limpeza automática de diretórios
    auto_cleanup_enabled: bool = True
    cleanup_days_to_keep: int = 30
    cleanup_on_startup: bool = True

    @classmethod
    def simple(cls, level: LogLevel = "INFO", log_dir: str = "logs") -> "LogConfig":
        """Create a simple logging configuration with minimal features."""
        return cls(
            level=level,
            log_dir=log_dir,
            console_enabled=True,
            file_enabled=True,
            json_format=False,
            colored_console=True,
            queue_enabled=False,
            rich_handler=False,
        )

    @classmethod
    def development(cls, level: LogLevel = "DEBUG", log_dir: str = "logs") -> "LogConfig":
        """Create a development-friendly logging configuration."""
        return cls(
            level=level,
            log_dir=log_dir,
            console_enabled=True,
            file_enabled=True,
            json_format=False,
            colored_console=True,
            queue_enabled=False,
            rich_handler=True,
        )

    @classmethod
    def production(cls, level: LogLevel = "INFO", log_dir: str = "logs") -> "LogConfig":
        """Create a production-ready logging configuration."""
        return cls(
            level=level,
            log_dir=log_dir,
            console_enabled=True,
            file_enabled=True,
            json_format=True,
            colored_console=False,
            queue_enabled=True,
            rich_handler=False,
            max_file_size=50,
            backup_count=10,
        )

    @classmethod
    def file_only(cls, level: LogLevel = "INFO", log_dir: str = "logs") -> "LogConfig":
        """Create a file-only logging configuration."""
        return cls(
            level=level,
            log_dir=log_dir,
            console_enabled=False,
            file_enabled=True,
            json_format=True,
            colored_console=False,
            queue_enabled=True,
            rich_handler=False,
        )

    @classmethod
    def console_only(cls, level: LogLevel = "INFO") -> "LogConfig":
        """Create a console-only logging configuration."""
        return cls(
            level=level,
            log_dir="",
            console_enabled=True,
            file_enabled=False,
            json_format=False,
            colored_console=True,
            queue_enabled=False,
            rich_handler=True,
        )

    def get_log_path(self) -> Path:
        """Get the Path object for the log directory."""
        return Path(self.log_dir)

    def ensure_log_dir(self) -> Path:
        """Ensure the log directory exists and return its Path."""
        log_path = self.get_log_path()
        log_path.mkdir(parents=True, exist_ok=True)
        return log_path
