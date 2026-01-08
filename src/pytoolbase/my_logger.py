from __future__ import annotations

import logging
import os
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .path_manipulations import PYTOOLBASE_ROOT_ENV


@dataclass(frozen=True)
class LoggerConfig:
    """Configuration for `get_logger`."""

    name: str
    level: int = logging.INFO
    console: bool = True
    log_dir: Path | None = None


def _resolve_log_dir(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit.expanduser().resolve()

    root = os.getenv(PYTOOLBASE_ROOT_ENV)
    if root:
        return (Path(root).expanduser().resolve() / "logs")

    return (Path.cwd().resolve() / "logs")


def get_logger(
    name: str,
    *,
    level: int = logging.INFO,
    console: bool = True,
    log_dir: Path | None = None,
) -> logging.Logger:
    """Return a logger configured with daily file + optional console handler.

    Notes
    -----
    - No directories are created implicitly: if the log directory does not exist,
      a `FileNotFoundError` is raised.
    - The function is idempotent for the same logger name (no duplicate handlers).
    """
    if not name.strip():
        raise ValueError("Logger name must be non-empty")

    resolved_dir = _resolve_log_dir(log_dir)
    if not resolved_dir.exists():
        raise FileNotFoundError(
            f"Log directory does not exist: {resolved_dir}. "
            "Create it (or set PYTOOLBASE_ROOT correctly)."
        )
    if not resolved_dir.is_dir():
        raise NotADirectoryError(f"Log directory is not a directory: {resolved_dir}")

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if getattr(logger, "_pytoolbase_configured", False):
        return logger

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    file_path = resolved_dir / f"{date.today():%Y-%m-%d}-{name}.log"
    file_handler = logging.FileHandler(file_path, mode="a", encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if console:
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    setattr(logger, "_pytoolbase_configured", True)
    return logger
