from __future__ import annotations

import json
import logging
import sys

from example_pkg.logging_utils import get_logger


def test_get_logger_plain(tmp_path, monkeypatch):
    monkeypatch.setenv("LOG_FORMAT", "plain")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    logger = get_logger("test.logger")
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.DEBUG
    # Ensure idempotency
    logger2 = get_logger("test.logger")
    assert logger.handlers and logger2.handlers
    assert logger.handlers[0] is logger2.handlers[0]


def test_get_logger_json(monkeypatch, capsys):
    monkeypatch.setenv("LOG_FORMAT", "json")
    monkeypatch.setenv("LOG_LEVEL", "INFO")
    logger = get_logger("json.logger")
    logger.info("hello", extra={"user": "alice"})
    captured = capsys.readouterr().out.strip()
    data = json.loads(captured)
    assert data["level"] == "INFO"
    assert data["message"] == "hello"
    assert data["user"] == "alice"


def test_plain_color_branch(monkeypatch, capsys):
    monkeypatch.setenv("LOG_FORMAT", "plain")
    monkeypatch.setenv("LOG_LEVEL", "WARNING")
    monkeypatch.setenv("LOG_COLOR", "1")
    # Force TTY to enable color branch
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True, raising=False)
    logger = get_logger("color.logger")
    logger.warning("colored")
    out = capsys.readouterr().out
    assert "colored" in out
    # Expect an ANSI escape sequence in output
    assert "\x1b[" in out


def test_root_logger(monkeypatch):
    monkeypatch.setenv("LOG_FORMAT", "plain")
    monkeypatch.setenv("LOG_LEVEL", "ERROR")
    root_logger = get_logger(None)
    assert isinstance(root_logger, logging.Logger)
    # Calling again should not add handlers
    root2 = get_logger(None)
    assert root_logger.handlers and root2.handlers
    assert root_logger.handlers[0] is root2.handlers[0]
