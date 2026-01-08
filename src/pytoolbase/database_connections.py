from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from ._optional import OptionalDependencyError, require_dependency
from .configuration_file import EnvFile
from .path_manipulations import PathContext


@dataclass(frozen=True)
class Db2ConnectionParams:
    """Parameters to connect to DB2 via JDBC (jt400)."""

    jdbc_driver: str
    jdbc_url_prefix: str
    host: str
    user: str
    password: str
    jt400_jar_path: Path
    prompt: bool = False

    def jdbc_url(self) -> str:
        url = f"{self.jdbc_url_prefix}{self.host}"
        if not self.prompt and "prompt=false" not in url.lower():
            sep = ";" if ";" in url else ";"
            url = f"{url}{sep}prompt=false"
        return url


def load_db2_params(
    *,
    country: str,
    environment: str,
    ctx: PathContext | None = None,
) -> Db2ConnectionParams:
    """Load DB2 connection parameters from env files in `PYTOOLBASE_ROOT`."""
    ctx = ctx or PathContext.from_env()

    general_env_path = ctx.general_env_file()
    country_env_path = ctx.country_env_file(country=country, environment=environment)

    general = EnvFile(general_env_path)
    country_env = EnvFile(country_env_path)

    jdbc_driver = general.require("jdbc_driver")
    jdbc_url_prefix = general.require("jdbc_url_prefix")

    # Prefer OS environment override.
    jar_override = general.get("JT400_JAR_PATH")  # allow in file too, but not encouraged
    jar_path_str = (
        jar_override
        or (general.get("jt400_jar_path") or None)
        or None
    )
    import os
    jar_path_str = os.getenv("JT400_JAR_PATH") or jar_path_str
    if not jar_path_str:
        raise KeyError(f"Missing required key 'jt400_jar_path' in env: {general_env_path}")

    jar_path = Path(jar_path_str).expanduser().resolve()
    if not jar_path.exists():
        raise FileNotFoundError(f"JT400 JAR not found: {jar_path}")

    host = country_env.require("db_host")
    user = country_env.require("db_user")
    password = country_env.require("db_password")

    return Db2ConnectionParams(
        jdbc_driver=jdbc_driver,
        jdbc_url_prefix=jdbc_url_prefix,
        host=host,
        user=user,
        password=password,
        jt400_jar_path=jar_path,
        prompt=False,
    )


def connect_jdbc(params: Db2ConnectionParams):
    """Connect using `jaydebeapi` (optional dependency)."""
    try:
        jaydebeapi = require_dependency("jaydebeapi", extra="db", feature="JDBC connections")
    except OptionalDependencyError as exc:
        raise exc

    return jaydebeapi.connect(
        params.jdbc_driver,
        params.jdbc_url(),
        [params.user, params.password],
        str(params.jt400_jar_path),
    )


def read_sql_file(sql_path: Path) -> str:
    sql_path = sql_path.expanduser().resolve()
    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")
    return sql_path.read_text(encoding="utf-8")


def execute_sql(conn: Any, sql: str, params: Iterable[Any] | None = None) -> int:
    """Execute a statement and commit (always)."""
    cursor = conn.cursor()
    try:
        if params is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, params)
        conn.commit()
        return getattr(cursor, "rowcount", -1)
    finally:
        cursor.close()


def query_rows(conn: Any, sql: str, params: Iterable[Any] | None = None) -> tuple[list[str], list[tuple[Any, ...]]]:
    """Run a query and return (columns, rows)."""
    cursor = conn.cursor()
    try:
        if params is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, params)
        rows = cursor.fetchall()
        cols = [d[0] for d in (cursor.description or [])]
        return cols, rows
    finally:
        cursor.close()


def query_dicts(conn: Any, sql: str, params: Iterable[Any] | None = None) -> list[dict[str, Any]]:
    cols, rows = query_rows(conn, sql, params=params)
    return [dict(zip(cols, row)) for row in rows]


def query_to_dataframe(conn: Any, sql: str, params: Any | None = None):
    """Run a query and return a pandas DataFrame (optional dependency)."""
    try:
        pd = require_dependency("pandas", extra="db", feature="pandas DataFrame queries")
    except OptionalDependencyError as exc:
        raise exc
    return pd.read_sql(sql, conn, params=params)
