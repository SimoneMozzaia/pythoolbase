from __future__ import annotations

import os
import sqlite3
from pathlib import Path

import pytest

from pytoolbase._optional import OptionalDependencyError
from pytoolbase.database_connections import (
    connect_jdbc,
    execute_sql,
    load_db2_params,
    query_dicts,
    query_rows,
)
from pytoolbase.path_manipulations import PYTOOLBASE_ROOT_ENV, PathContext


def test_load_db2_params(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange pytoolbase root structure (no auto-creation in code)
    (tmp_path / "env").mkdir()
    (tmp_path / "logs").mkdir()

    jar = tmp_path / "jt400.jar"
    jar.write_text("dummy", encoding="utf-8")

    (tmp_path / "env" / ".env").write_text(
        "jdbc_driver=com.ibm.as400.access.AS400JDBCDriver\n"
        "jdbc_url_prefix=jdbc:as400://\n"
        f"jt400_jar_path={jar.as_posix()}\n",
        encoding="utf-8",
    )

    (tmp_path / "env" / ".IT-prod-env").write_text(
        "db_host=server1\n"
        "db_user=user1\n"
        "db_password=pass1\n",
        encoding="utf-8",
    )

    monkeypatch.setenv(PYTOOLBASE_ROOT_ENV, str(tmp_path))

    params = load_db2_params(country="IT", environment="prod")
    assert params.host == "server1"
    assert params.jdbc_driver
    assert params.jt400_jar_path == jar.resolve()


def test_connect_jdbc_requires_jaydebeapi(tmp_path: Path) -> None:
    params = type("P", (), {
        "jdbc_driver": "x",
        "jdbc_url": lambda self: "y",
        "user": "u",
        "password": "p",
        "jt400_jar_path": tmp_path / "jt400.jar",
    })()
    with pytest.raises(OptionalDependencyError):
        connect_jdbc(params)  # type: ignore[arg-type]


def test_query_rows_query_dicts_and_execute_sql() -> None:
    conn = sqlite3.connect(":memory:")
    try:
        execute_sql(conn, "CREATE TABLE t (id INTEGER, name TEXT)")
        execute_sql(conn, "INSERT INTO t (id, name) VALUES (?, ?)", (1, "a"))
        execute_sql(conn, "INSERT INTO t (id, name) VALUES (?, ?)", (2, "b"))

        cols, rows = query_rows(conn, "SELECT id, name FROM t ORDER BY id")
        assert cols == ["id", "name"]
        assert rows == [(1, "a"), (2, "b")]

        dicts = query_dicts(conn, "SELECT id, name FROM t ORDER BY id")
        assert dicts == [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]
    finally:
        conn.close()
