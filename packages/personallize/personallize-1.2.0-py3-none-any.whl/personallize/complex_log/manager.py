"""Advanced logging manager with comprehensive configuration support.

This module provides the LogManager class that handles logger creation,
configuration, and management with support for various output formats,
handlers, and advanced features.

Usage Examples:

    Basic usage with default configuration:
        >>> manager = LogManager()
        >>> logger, exception_decorator = manager.get_logger()
        >>> logger.info("Application started")

    Custom configuration:
        >>> from .config import LogConfig
        >>> config = LogConfig(level="DEBUG", log_dir="debug_logs")
        >>> manager = LogManager(config)
        >>> logger, decorator = manager.get_simple_logger("debug_app")
        >>> logger.debug("Debug information")

    File-specific logging:
        >>> logger, decorator = manager.get_simple_logger("app", "app.log")
        >>> logger.warning("This goes to app.log")

    Using exception decorator:
        >>> logger, exception_decorator = manager.get_logger()
        >>> @exception_decorator
        ... def risky_operation():
        ...     return 1 / 0
        >>> risky_operation()  # Exception logged automatically

Features:
    - Multiple output formats (JSON, plain text, colored console)
    - File rotation with size limits and backup counts
    - Asynchronous logging with queue handlers
    - Rich console output with enhanced formatting
    - Automatic exception logging with decorators
    - Compatible interface with simple_log module
    - Thread-safe logger management
    - Customizable log directories and file names
"""

import functools
import logging
import logging.handlers
import os
import sys
import traceback
import uuid
from collections.abc import Callable
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import Any

try:
    from rich.console import Console

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from .config import LogConfig
from .formatters import DetailedFileFormatter, FileFormatter, JSONLogFormatter, RichIconFormatter


class LogManager:
    """
    LogManager simplificado para complex_log usando apenas LogConfig.
    Interface compatível com simple_log sem dependências de JSON.
    """

    def __init__(self, config: LogConfig | None = None):
        """
        Inicializa o LogManager com uma configuração.

        Args:
            config: Configuração de logging. Se None, usa LogConfig.simple()
        """
        self.config = config or LogConfig.simple()
        self._loggers = {}
        self._setup_done = False

    def _cleanup_old_log_directories(self, base_dir: str = "logs") -> None:
        """
        Remove diretórios de logs antigos baseado na configuração.

        Args:
            base_dir: Diretório base onde estão os logs organizados por data
        """
        if not self.config.auto_cleanup_enabled:
            return

        base_path = Path(base_dir)
        if not base_path.exists():
            return

        # Data limite para manter diretórios
        cutoff_date = datetime.now() - timedelta(days=self.config.cleanup_days_to_keep)

        # Percorrer diretórios no formato dd_mm_yyyy
        for dir_path in base_path.iterdir():
            if not dir_path.is_dir():
                continue

            try:
                # Tentar parsear o nome do diretório como data
                dir_date = datetime.strptime(dir_path.name, "%d_%m_%Y")

                # Se o diretório é mais antigo que o limite, remover
                if dir_date < cutoff_date:
                    import shutil

                    shutil.rmtree(dir_path)
                    print(f"Removed old log directory: {dir_path}")

            except ValueError:
                # Ignorar diretórios que não seguem o padrão de data
                continue

    def _setup_basic_logging(self) -> None:
        """Configura logging básico baseado no LogConfig."""
        if self._setup_done:
            return

        # Converter nível de string para int se necessário
        if isinstance(self.config.level, str):
            level_map = {
                "DEBUG": logging.DEBUG,
                "INFO": logging.INFO,
                "WARNING": logging.WARNING,
                "ERROR": logging.ERROR,
                "CRITICAL": logging.CRITICAL,
            }
            config_level = level_map.get(self.config.level, logging.INFO)
        else:
            config_level = self.config.level

        # Configurar nível root
        logging.getLogger().setLevel(config_level)

        # Limpar handlers existentes se necessário
        if not self.config.propagate:
            logging.getLogger().handlers.clear()

        self._setup_done = True

    def _create_file_handler(self, log_file: str, level: int) -> logging.FileHandler | None:
        """Cria um handler de arquivo se configurado."""
        if not self.config.file_enabled:
            return None

        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setLevel(level)

        # Formato baseado no LogConfig - usar formatter detalhado para arquivo
        if self.config.format_string:
            formatter = DetailedFileFormatter(datefmt=self.config.date_format)
            handler.setFormatter(formatter)

        return handler

    def _create_console_handler(self, level: int) -> logging.StreamHandler | None:
        """Cria um handler de console se configurado."""
        if not self.config.console_enabled:
            return None

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        # Formato baseado no LogConfig
        if self.config.format_string:
            formatter = RichIconFormatter(
                self.config.format_string, datefmt=self.config.date_format
            )
            handler.setFormatter(formatter)

        return handler

    def setup_logger(
        self,
        name: str = "app",
        log_file: str | None = None,
        level: int = logging.INFO,
        config: LogConfig | None = None,
    ) -> logging.Logger:
        """
        Setup a logger with the given configuration.
        Maintains compatibility with simple_log interface.

        Args:
            name: Logger name
            log_file: Optional log file path (for compatibility)
            level: Logging level
            config: Optional LogConfig object for advanced configuration

        Returns:
            Configured logger instance
        """
        self._setup_basic_logging()

        # Usar config específico se fornecido
        current_config = config or self.config

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.propagate = current_config.propagate

        # Limpar handlers existentes
        logger.handlers.clear()

        # Adicionar handler de arquivo se necessário
        if log_file and current_config.file_enabled:
            file_handler = self._create_file_handler(log_file, level)
            if file_handler:
                logger.addHandler(file_handler)

        # Adicionar handler de console se necessário
        if current_config.console_enabled:
            console_handler = self._create_console_handler(level)
            if console_handler:
                logger.addHandler(console_handler)

        self._loggers[name] = logger
        return logger

    def exception(self, logger: logging.Logger):
        """
        Decorator for logging exceptions with detailed traceback information.
        Maintains the same interface as simple_log.

        Args:
            logger: Logger instance to use for exception logging

        Returns:
            Decorator function
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    tb = traceback.extract_tb(e.__traceback__)
                    filename, lineno, function_name, _ = tb[-1]

                    log_message = (
                        f"An exception occurred...\n"
                        f"Type: {type(e).__name__}\n"
                        f"Message: {e}\n"
                        f"Location:\n"
                        f" - File: {filename}\n"
                        f" - Line: {lineno}\n"
                        f" - Function: {func.__name__}\n\n"
                    )

                    logger.error(log_message)
                    raise  # Re-raise the exception

            return wrapper

        return decorator

    def get_logger(
        self, name: str, another_directory: str | None = None, config: LogConfig | None = None
    ) -> tuple[logging.Logger, Any]:
        """
        Get a configured logger with automatic file naming based on current date/time.
        Maintains compatibility with simple_log interface.

        Args:
            another_directory: Optional directory for log files
            config: Optional LogConfig for advanced configuration

        Returns:
            Tuple of (logger, exception_decorator)
        """
        # Use provided config or use the instance config
        current_config = config or self.config

        # Executar limpeza automática se habilitada
        base_dir = another_directory if another_directory else "logs"
        if current_config.cleanup_on_startup:
            self._cleanup_old_log_directories(base_dir)

        # Create log directory structure similar to simple_log
        day = datetime.now().strftime("%d_%m_%Y")
        date_path = Path(f"{base_dir}/{day}")
        date_path.mkdir(parents=True, exist_ok=True)

        # Format timestamp for filename
        time_stamp = datetime.now().strftime("%H_%M")
        log_file_path = date_path / f"{time_stamp}.log"

        # Setup logger
        logger = self.setup_logger(
            name=name,
            log_file=str(log_file_path),
            level=logging.DEBUG,
            config=current_config,
        )

        return (logger, self.exception)

    def get_logger_with_config(
        self, config: LogConfig, logger_name: str = "complex_logger"
    ) -> tuple[logging.Logger, Any]:
        """
        Get a logger with explicit LogConfig configuration.
        This is an additional method specific to complex_log for advanced usage.

        Args:
            config: LogConfig object with desired configuration
            logger_name: Name for the logger

        Returns:
            Tuple of (logger, exception_decorator)
        """
        # Ensure log directory exists
        if config.file_enabled and config.log_dir:
            config.ensure_log_dir()

        # Setup logger with config
        logger = self.setup_logger(name=logger_name, config=config)

        return (logger, self.exception)

    def get_simple_logger(
        self,
        name: str | None = None,
        log_file: str | None = None,
        config: LogConfig | None = None,
    ) -> tuple[logging.Logger, Callable]:
        """
        Obtém um logger configurado e um decorator de exceção.
        Interface compatível com simple_log.LogManager.

        Args:
            name: Nome do logger (opcional, usa nome automático se None)
            log_file: Caminho do arquivo de log (opcional)
            config: Configuração específica (opcional)

        Returns:
            Tupla (logger, exception_decorator)
        """
        # Gerar nome automático se não fornecido
        if name is None:
            import inspect

            frame = inspect.currentframe().f_back
            module_name = frame.f_globals.get("__name__", "unknown")
            name = f"{module_name}_auto"

        # Gerar caminho de arquivo automático se necessário
        if log_file is None and (config or self.config).file_enabled:
            logs_dir = Path("logs")
            log_file = str(logs_dir / f"{name}.log")

        # Converter nível de string para int se necessário
        current_config = config or self.config
        if isinstance(current_config.level, str):
            level_map = {
                "DEBUG": logging.DEBUG,
                "INFO": logging.INFO,
                "WARNING": logging.WARNING,
                "ERROR": logging.ERROR,
                "CRITICAL": logging.CRITICAL,
            }
            config_level = level_map.get(current_config.level, logging.INFO)
        else:
            config_level = current_config.level

        # Configurar logger
        logger = self.setup_logger(name=name, log_file=log_file, level=config_level, config=config)

        # Criar decorator de exceção simples
        def exception_decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.exception("Erro em %s", func.__name__)
                    raise

            return wrapper

        return logger, exception_decorator
