"""Logging helpers: consistent formatter, JSON/plain modes, and color support.

This module provides a single entrypoint, ``get_logger``, which returns a configured
``logging.Logger`` with a robust formatter:

- Plain format: ``YYYY-MM-DDTHH:MM:SS.mmmZ | LEVEL | name:lineno - message``
- JSON format: ``{"time": ..., "level": ..., "logger": ..., "line": ..., "message": ...}``

Configuration (environment variables):
- ``LOG_LEVEL``: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)
- ``LOG_FORMAT``: ``plain`` (default) or ``json``
- ``LOG_COLOR``: ``1`` to enable ANSI color in plain mode (default: off)

Notes
-----
The logger is configured only once per name; repeat calls return the same logger without
duplicating handlers.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from typing import Any, Dict

ISO_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"


def _level_from_env(default: str = "INFO") -> int:
    level_name = os.getenv("LOG_LEVEL", default).upper()
    return getattr(logging, level_name, logging.INFO)


def _use_json() -> bool:
    return os.getenv("LOG_FORMAT", "plain").lower() == "json"


def _use_color() -> bool:
    return os.getenv("LOG_COLOR", "0") in {"1", "true", "yes", "on"}


class PlainFormatter(logging.Formatter):
    """Plain text formatter with optional ANSI color for levels."""

    base_fmt = "%(asctime)s | %(levelname)s | %(name)s:%(lineno)d - %(message)s"

    _COLORS = {
        "DEBUG": "\x1b[36m",  # cyan
        "INFO": "\x1b[32m",  # green
        "WARNING": "\x1b[33m",  # yellow
        "ERROR": "\x1b[31m",  # red
        "CRITICAL": "\x1b[35m",  # magenta
    }
    _RESET = "\x1b[0m"

    def __init__(self, *, color: bool = False) -> None:
        super().__init__(fmt=self.base_fmt, datefmt=ISO_FMT)
        self._color = color and sys.stdout.isatty()

    def format(self, record: logging.LogRecord) -> str:  # noqa: D401
        """Format the record; apply color to the level name if enabled."""
        if self._color:
            level = record.levelname
            if level in self._COLORS:
                record.levelname = f"{self._COLORS[level]}{level}{self._RESET}"
                try:
                    return super().format(record)
                finally:
                    record.levelname = level  # restore
        return super().format(record)


class JsonFormatter(logging.Formatter):
    """Minimal JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:  # noqa: D401
        """Format the record as a JSON object."""
        data: Dict[str, Any] = {
            "time": self.formatTime(record, datefmt=ISO_FMT),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        # Attach extras if provided (fields added via LoggerAdapter or extra=...)
        for k, v in record.__dict__.items():
            if k in {
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
            }:
                continue
            if k not in data:
                try:
                    json.dumps(v)
                except Exception:
                    continue
                data[k] = v
        return json.dumps(data, separators=(",", ":"))


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a configured logger with a single StreamHandler.

    Parameters
    ----------
    name
        Logger name. ``None`` returns the root logger.

    Returns
    -------
    logging.Logger
        Configured logger using plain or JSON formatting as per env vars.
    """
    logger = logging.getLogger(name)
    if getattr(logger, "_configured_by_template", False):
        return logger

    logger.setLevel(_level_from_env())
    handler = logging.StreamHandler(stream=sys.stdout)
    if _use_json():
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(PlainFormatter(color=_use_color()))

    # Avoid duplicate handlers if called multiple times.
    logger.handlers = [h for h in logger.handlers if not isinstance(h, logging.StreamHandler)]
    logger.addHandler(handler)
    logger.propagate = False

    setattr(logger, "_configured_by_template", True)
    return logger


__all__ = ["get_logger", "PlainFormatter", "JsonFormatter"]
