"""CLI builder and main entry point."""

from __future__ import annotations

import click

from artificer.cli.config import ArtificerConfig, load_config
from artificer.cli.loader import import_builtin_module, load_custom_modules


def build_cli(config: ArtificerConfig | None = None) -> click.Group:
    """Build the Artificer CLI with all registered modules.

    Args:
        config: Optional configuration. If not provided, loads from pyproject.toml.

    Returns:
        Configured Click command group.
    """
    if config is None:
        config = load_config()

    @click.group()
    @click.version_option(package_name="artificer-cli")
    def cli() -> None:
        """Artificer Command Line Interface."""
        pass

    # Register built-in modules (in order)
    for feature in config.features:
        try:
            module_class = import_builtin_module(feature)
            module_class.register(cli, config)
        except RuntimeError as e:
            # Re-raise with context about which feature failed
            raise RuntimeError(f"Failed to load feature '{feature}': {e}") from e

    # Register custom modules from entrypoint
    if config.entrypoint:
        try:
            custom_modules = load_custom_modules(config.entrypoint)
            for module_class in custom_modules:
                module_class.register(cli, config)
        except RuntimeError as e:
            raise RuntimeError(
                f"Failed to load custom modules from '{config.entrypoint}': {e}"
            ) from e

    return cli


def main() -> None:
    """Main entry point for the Artificer CLI."""
    cli = build_cli()
    cli()


if __name__ == "__main__":
    main()
