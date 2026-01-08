from __future__ import annotations

import json
from pathlib import Path

import pytest

from pytoolbase.configuration_file import EnvFile, read_json_value


def test_envfile_get_require_and_set(tmp_path: Path) -> None:
    env_path = tmp_path / ".env"
    env_path.write_text("FOO=bar\nEMPTY=\n", encoding="utf-8")

    env = EnvFile(env_path)
    assert env.get("FOO") == "bar"
    assert env.get("MISSING") is None
    assert env.get("MISSING", default="x") == "x"
    assert env.require("FOO") == "bar"
    with pytest.raises(KeyError):
        env.require("MISSING")

    env.set("FOO", "baz")
    assert EnvFile(env_path).require("FOO") == "baz"


def test_read_json_value(tmp_path: Path) -> None:
    j = tmp_path / "data.json"
    j.write_text(json.dumps({"a": {"b": 1}, "x": 2}), encoding="utf-8")

    assert read_json_value(j, "x") == 2
    assert read_json_value(j, "a", "b") == 1

    with pytest.raises(KeyError):
        read_json_value(j, "missing")

    with pytest.raises(KeyError):
        read_json_value(j, "a", "missing")

    with pytest.raises(FileNotFoundError):
        read_json_value(tmp_path / "nope.json", "x")
