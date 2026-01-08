from __future__ import annotations

import os
from pathlib import Path

import pytest

from pytoolbase.path_manipulations import PYTOOLBASE_ROOT_ENV, PathContext, build_country_env_filename


def test_build_country_env_filename() -> None:
    assert build_country_env_filename(country="IT", environment="prod") == ".IT-prod-env"
    with pytest.raises(ValueError):
        build_country_env_filename(country="", environment="prod")


def test_path_context_from_env_no_dir_creation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(PYTOOLBASE_ROOT_ENV, str(tmp_path))

    ctx = PathContext.from_env()
    assert ctx.root == tmp_path.resolve()
    # must not create dirs
    assert not (tmp_path / "env").exists()
    assert ctx.general_env_file() == tmp_path / "env" / ".env"
    assert ctx.country_env_file(country="IT", environment="prod") == tmp_path / "env" / ".IT-prod-env"


def test_path_context_requires_existing_root(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(PYTOOLBASE_ROOT_ENV, r"C:\this_should_not_exist_12345")
    with pytest.raises(FileNotFoundError):
        PathContext.from_env()
