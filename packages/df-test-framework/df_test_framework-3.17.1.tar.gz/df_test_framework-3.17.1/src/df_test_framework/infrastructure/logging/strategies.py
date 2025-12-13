"""
Logging strategies configure log handlers and return a ready-to-use Logger.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from loguru._logger import Logger

from ..config.schema import LoggingConfig
from .logger import is_logger_configured, logger, setup_logger


class LoggerStrategy(Protocol):
    def configure(self, config: LoggingConfig) -> Logger: ...


@dataclass
class LoguruStructuredStrategy:
    """
    Default Loguru strategy: supports console + file output with sanitisation.
    """

    def configure(self, config: LoggingConfig) -> Logger:
        setup_logger(
            log_level=config.level,
            log_file=config.file,
            rotation=config.rotation,
            retention=config.retention,
            enable_console=config.enable_console,
            enable_sanitize=config.sanitize,
        )
        return logger


@dataclass
class NoOpStrategy:
    """
    Strategy that leaves logging untouched and simply returns the global logger.
    """

    def configure(self, config: LoggingConfig) -> Logger:
        if not is_logger_configured():
            # Configure logger minimally if nothing has been done yet.
            setup_logger(
                log_level=config.level,
                log_file=None,
                enable_console=config.enable_console,
                enable_sanitize=config.sanitize,
            )
        return logger
