from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, TypeVar

from dotenv import dotenv_values, set_key

T = TypeVar("T")


@dataclass(frozen=True)
class EnvFile:
    """A small wrapper around dotenv files.

    Behavior:
    - OS environment variables override file values (if present).
    - Values are returned as strings by default.

    Parameters
    ----------
    path:
        Path to the dotenv file.
    """

    path: Path

    def as_dict(self) -> dict[str, str]:
        values = dotenv_values(self.path)
        # dotenv_values can return None values for keys without values; normalize.
        normalized = {k: (v if v is not None else "") for k, v in values.items()}
        # Cast to str for typing consistency.
        return {str(k): str(v) for k, v in normalized.items()}

    def get(self, key: str, default: T | None = None, *, cast: Callable[[str], T] | None = None) -> T | None:
        if key in os.environ:
            raw = os.environ[key]
        else:
            raw = self.as_dict().get(key)

        if raw is None or raw == "":
            return default

        if cast is None:
            return raw  # type: ignore[return-value]
        return cast(raw)

    def require(self, key: str, *, cast: Callable[[str], T] | None = None) -> T:
        value = self.get(key, default=None, cast=cast)
        if value is None:
            raise KeyError(f"Missing required key '{key}' in env: {self.path}")
        return value

    def set(self, key: str, value: str) -> None:
        """Set (or update) a key in the dotenv file."""
        if not self.path.exists():
            raise FileNotFoundError(f"Env file not found: {self.path}")
        set_key(str(self.path), key, value)


def read_json_value(json_file: Path, key: str, sub_key: str | None = None) -> Any:
    """Read a value from a JSON file.

    If `sub_key` is provided, reads `data[key][sub_key]`.
    """
    if not json_file.exists():
        raise FileNotFoundError(f"JSON file not found: {json_file}")

    try:
        data = json.loads(json_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise json.JSONDecodeError(exc.msg, exc.doc, exc.pos)

    if sub_key is None:
        try:
            return data[key]
        except KeyError as exc:
            raise KeyError(f"Key '{key}' not found in JSON: {json_file}") from exc

    try:
        return data[key][sub_key]
    except KeyError as exc:
        raise KeyError(f"Key '{key}.{sub_key}' not found in JSON: {json_file}") from exc
