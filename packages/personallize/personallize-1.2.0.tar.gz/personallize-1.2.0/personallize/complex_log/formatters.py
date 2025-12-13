# Aula 11
# Como criar um Formatter JSON do zero para Python Logging - Aula 11
# https://youtu.be/jX4Ai-ZWkj4
#
# Playlist:
# https://www.youtube.com/playlist?list=PLbIBj8vQhvm28qR-yvWP3JELGelWxsxaI
#
# Artigo:
#
# https://www.otaviomiranda.com.br/2025/logging-no-python-pare-de-usar-print-no-lugar-errado/#criando-um-json-log-formatter

import json
import logging
from datetime import datetime
from typing import Any, override
from zoneinfo import ZoneInfo

from rich.console import Console

# Constantes de Configuração
# Define o fuso horário para os logs, garantindo consistência independente do servidor.
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TZ_IDENTIFIER = "America/Sao_Paulo"
try:
    TZ = ZoneInfo(TZ_IDENTIFIER)
except Exception:
    # Fallback para timezone local se ZoneInfo não estiver disponível
    import datetime

    TZ = datetime.timezone.utc

# Mapeamento de níveis de log para cores no terminal
LEVEL_COLORS = {
    "DEBUG": "blue",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold red",
}

# Mapeamento de níveis de log para texto simples
LEVEL_ICONS = {
    "DEBUG": "DEBUG",
    "INFO": "INFO",
    "WARNING": "WARNING",
    "ERROR": "ERROR",
    "CRITICAL": "CRITICAL",
}

LOG_RECORD_KEYS = [
    "name",
    "msg",
    "args",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
    "taskName",
    "message",
]


class JSONLogFormatter(logging.Formatter):
    def __init__(
        self,
        include_keys: list[str] | None = None,
        datefmt: str = "%Y-%m-%d %H:%M:%S",
    ) -> None:
        super().__init__()
        self.include_keys = include_keys if include_keys is not None else LOG_RECORD_KEYS
        self.datefmt = datefmt

    @override
    def format(self, record: logging.LogRecord) -> str:
        dict_record: dict[str, Any] = {
            key: getattr(record, key)
            for key in self.include_keys
            if key in LOG_RECORD_KEYS and getattr(record, key, None) is not None
        }

        if "created" in dict_record:
            # Sobrescrevi o método `formatTime` para retornar um datetime
            # ao invés de `struct_time` que é o padrão. Assim consigo trabalhar
            # com timezone.
            dict_record["created"] = self.formatTime(record, self.datefmt)

        if "message" in self.include_keys:
            dict_record["message"] = record.getMessage()

        if "exc_info" in dict_record and record.exc_info:
            # `exc_info` traz informações sobre exceções. Precisamos formatar
            # esse valor para uma string. Por sorte isso existe em `Formatter`.
            dict_record["exc_info"] = self.formatException(record.exc_info)

        if "stack_info" in dict_record and record.stack_info:
            dict_record["stack_info"] = self.formatStack(record.stack_info)

        for key, val in vars(record).items():
            if key in LOG_RECORD_KEYS:
                continue

            if key not in self.include_keys:
                msg = f'Key {key!r} does not exist in "include_keys"'
                raise KeyError(msg)

            dict_record[key] = val

        return json.dumps(dict_record, default=str)

    @override
    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        date = datetime.fromtimestamp(record.created, tz=TZ)

        if datefmt:
            return date.strftime(datefmt)

        return date.isoformat()


class DetailedFileFormatter(logging.Formatter):
    """
    Formatador detalhado para arquivos de log com informações relevantes.
    Não usa Rich para evitar códigos de escape ANSI no arquivo.
    """

    def __init__(self, fmt: str | None = None, datefmt: str | None = None) -> None:
        # Formato detalhado para arquivo
        if fmt is None:
            fmt = "%(asctime)s | %(levelname)s | %(message)s | file: %(filename)s:%(lineno)d | func: %(funcName)s | module: %(module)s | process: %(processName)s:%(process)d | thread: %(threadName)s:%(thread)d"
        if datefmt is None:
            datefmt = "%Y-%m-%d %H:%M:%S"
        super().__init__(fmt, datefmt)

    @override
    def format(self, record: logging.LogRecord) -> str:
        """
        Formata o registro de log com informações detalhadas para arquivo.
        """
        # Usa o formatador da classe base para criar a mensagem de log
        formatted = super().format(record)

        # Adiciona informações de exceção se existirem
        if record.exc_info and not record.exc_text:
            record.exc_text = self.formatException(record.exc_info)
            if record.exc_text:
                formatted += "\n" + record.exc_text

        # Adiciona informações de stack se existirem
        if record.stack_info:
            formatted += "\n" + self.formatStack(record.stack_info)

        return formatted


class FileFormatter(logging.Formatter):
    """
    Formatador simples para arquivos de log.
    Não usa Rich para evitar códigos de escape ANSI no arquivo.
    """

    @override
    def format(self, record: logging.LogRecord) -> str:
        # Adiciona o ícone do nível ao record com espaçamento adequado
        icon = LEVEL_ICONS.get(record.levelname, record.levelname)
        record.levelname_icon = f"{icon} "

        return super().format(record)


class RichIconFormatter(logging.Formatter):
    """
    Formatador de log com ícones usando Rich de forma simples.
    Formato: [datetime] ícone msg
    """

    def __init__(self, fmt: str | None = None, datefmt: str | None = None) -> None:
        if fmt is None:
            fmt = "[%(asctime)s] %(levelname_icon)s %(message)s"
        if datefmt is None:
            datefmt = "%Y-%m-%d %H:%M:%S"
        super().__init__(fmt, datefmt)
        self.console = Console()

    @override
    def format(self, record: logging.LogRecord) -> str:
        level_text = LEVEL_ICONS.get(record.levelname, record.levelname)
        color = LEVEL_COLORS.get(record.levelname, "white")

        with self.console.capture() as capture:
            self.console.print(level_text, style=color, end="")
        colored_level = capture.get()

        record.levelname_icon = colored_level

        return super().format(record)


class IconFormatter(logging.Formatter):
    def __init__(self, fmt: str | None = None, datefmt: str | None = None) -> None:
        if fmt is None:
            fmt = "[%(asctime)s] %(levelname_icon)s %(message)s"
        if datefmt is None:
            datefmt = "%Y-%m-%d %H:%M:%S"
        super().__init__(fmt, datefmt)

    @override
    def format(self, record: logging.LogRecord) -> str:
        """
        Formata o registro de log substituindo o levelname pelo ícone correspondente.
        """
        # Adiciona o ícone do nível ao record com espaçamento adequado
        icon = LEVEL_ICONS.get(record.levelname, record.levelname)
        record.levelname_icon = f"{icon} "  # Adiciona espaço após o ícone

        # Usa o formatador da classe base para criar a mensagem de log
        return super().format(record)
