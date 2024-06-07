"""Настройки логера"""

from __future__ import annotations

from logging import (
    Formatter,
    Logger,
    StreamHandler,
    getLogger,
)

__all__ = ("get_logger",)


def get_logger(level: str = "INFO") -> Logger:
    """
    Настройка логирования

    Args:
        level: Уровень логирования. Defaults to INFO.

    Returns:
        Экземпляр :class: `Logger`
    """
    # Create a custom logger
    logger = getLogger(__name__)
    logger.setLevel(level)

    c_format = Formatter(
        "%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

    # Create handlers
    c_handler = StreamHandler()

    # Create formatters and add it to handlers
    c_handler.setFormatter(c_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)

    return logger
