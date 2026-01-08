from __future__ import annotations

import logging
import os
from pathlib import Path

import pytest

from pytoolbase.my_logger import get_logger
from pytoolbase.path_manipulations import PYTOOLBASE_ROOT_ENV


def test_get_logger_requires_log_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(PYTOOLBASE_ROOT_ENV, str(tmp_path))
    # logs dir missing
    with pytest.raises(FileNotFoundError):
        get_logger("test")


def test_get_logger_daily_file_and_idempotent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "logs").mkdir()
    monkeypatch.setenv(PYTOOLBASE_ROOT_ENV, str(tmp_path))

    logger = get_logger("unit", level=logging.INFO, console=True)
    logger.info("hello")

    # At least one FileHandler should exist and point into logs dir
    file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
    assert file_handlers
    assert Path(file_handlers[0].baseFilename).parent == (tmp_path / "logs").resolve()

    # Calling again should not add handlers
    before = len(logger.handlers)
    logger2 = get_logger("unit", level=logging.INFO, console=True)
    assert logger2 is logger
    assert len(logger.handlers) == before
