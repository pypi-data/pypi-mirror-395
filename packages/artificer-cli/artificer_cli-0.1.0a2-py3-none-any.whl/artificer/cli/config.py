"""Configuration loading from pyproject.toml."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


@dataclass
class ArtificerConfig:
    """Configuration for Artificer CLI."""

    features: list[str]
    entrypoint: str | None


def load_config(base_path: Path | None = None) -> ArtificerConfig:
    """Load configuration from pyproject.toml.

    Args:
        base_path: Directory containing pyproject.toml. Defaults to CWD.

    Returns:
        ArtificerConfig with parsed configuration.

    Raises:
        RuntimeError: If config file is missing or invalid.
    """
    if base_path is None:
        base_path = Path.cwd()

    pyproject_path = base_path / "pyproject.toml"

    if not pyproject_path.exists():
        raise RuntimeError(
            f"pyproject.toml not found in {base_path}. "
            "Artificer requires a pyproject.toml file with [tool.artificer] section."
        )

    with open(pyproject_path, "rb") as f:
        try:
            data = tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            raise RuntimeError(f"Failed to parse pyproject.toml: {e}") from e

    tool_config = data.get("tool", {})
    artificer_config = tool_config.get("artificer")

    if artificer_config is None:
        raise RuntimeError(
            "Missing [tool.artificer] section in pyproject.toml. "
            "Add a [tool.artificer] section with 'features' and optional 'entrypoint'."
        )

    features = artificer_config.get("features")
    if features is None:
        raise RuntimeError(
            "Missing 'features' in [tool.artificer]. "
            "Add 'features = []' or 'features = [\"workflows\"]' to enable modules."
        )

    if not isinstance(features, list):
        raise RuntimeError(
            f"'features' must be a list, got {type(features).__name__}."
        )

    entrypoint = artificer_config.get("entrypoint")
    if entrypoint is not None and not isinstance(entrypoint, str):
        raise RuntimeError(
            f"'entrypoint' must be a string, got {type(entrypoint).__name__}."
        )

    return ArtificerConfig(features=features, entrypoint=entrypoint)
