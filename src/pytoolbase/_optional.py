from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OptionalDependencyError(ImportError):
    """Raised when an optional dependency is required but not installed."""

    dependency: str
    extra: str
    feature: str

    def __str__(self) -> str:
        return (
            f"Optional dependency '{self.dependency}' is required for {self.feature}. "
            f"Install with: pip install 'pytoolbase[{self.extra}]'"
        )


def require_dependency(module_name: str, *, extra: str, feature: str):
    """Import and return an optional module, raising a clear error if missing."""
    try:
        module = __import__(module_name)
    except ModuleNotFoundError as exc:
        raise OptionalDependencyError(module_name, extra, feature) from exc
    return module
