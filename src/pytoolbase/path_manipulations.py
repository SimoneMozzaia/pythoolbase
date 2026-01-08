from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PYTOOLBASE_ROOT_ENV = "PYTOOLBASE_ROOT"


def build_country_env_filename(*, country: str, environment: str) -> str:
    """Build the country-specific .env file name.

    Convention:
        .<COUNTRY>-<ENV>-env

    Example:
        .IT-prod-env
    """
    country_clean = country.strip()
    env_clean = environment.strip()
    if not country_clean or not env_clean:
        raise ValueError("country and environment must be non-empty")
    return f".{country_clean}-{env_clean}-env"


@dataclass(frozen=True)
class PathContext:
    """Resolved filesystem locations for pytoolbase conventions.

    No directory is created implicitly: if your workflow requires folders, you must
    provision them out-of-band (e.g., repo checkout, NAS structure, manual setup).
    """

    root: Path
    env_dir: Path
    secrets_dir: Path
    queries_dir: Path
    logs_dir: Path

    @classmethod
    def from_root(cls, root: Path) -> "PathContext":
        root = root.expanduser().resolve()
        if not root.exists():
            raise FileNotFoundError(f"PYTOOLBASE root does not exist: {root}")
        if not root.is_dir():
            raise NotADirectoryError(f"PYTOOLBASE root is not a directory: {root}")
        return cls(
            root=root,
            env_dir=root / "env",
            secrets_dir=root / "secrets",
            queries_dir=root / "queries",
            logs_dir=root / "logs",
        )

    @classmethod
    def from_env(cls) -> "PathContext":
        value = os.getenv(PYTOOLBASE_ROOT_ENV)
        if not value:
            raise EnvironmentError(
                f"Missing environment variable {PYTOOLBASE_ROOT_ENV}. "
                "Set it to the pytoolbase root folder."
            )
        return cls.from_root(Path(value))

    def general_env_file(self) -> Path:
        return self.env_dir / ".env"

    def country_env_file(self, *, country: str, environment: str) -> Path:
        return self.env_dir / build_country_env_filename(country=country, environment=environment)

    def token_file(self) -> Path:
        return self.secrets_dir / "token.json"

    def user_oauth_credentials_file(self) -> Path:
        return self.secrets_dir / "oauth2_client_user_not_service.json"

    def service_account_credentials_file(self) -> Path:
        return self.secrets_dir / "service_account.json"

    def sql_file(self, filename: str) -> Path:
        filename_clean = filename.strip()
        if not filename_clean:
            raise ValueError("filename must be non-empty")
        return self.queries_dir / filename_clean
