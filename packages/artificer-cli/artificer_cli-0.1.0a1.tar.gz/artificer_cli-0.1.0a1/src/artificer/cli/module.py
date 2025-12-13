"""ArtificerModule base class and built-in module registry."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import click
    from artificer.cli.config import ArtificerConfig


class ArtificerModule:
    """Base class for Artificer modules.

    Modules extend the CLI by registering commands and initializing subsystems.
    All functionality should be contained within the register() method.
    """

    @classmethod
    def register(cls, cli: click.Group, config: ArtificerConfig) -> None:
        """Register this module with the CLI.

        Args:
            cli: The root Click command group to extend.
            config: The Artificer configuration.

        Raises:
            NotImplementedError: Subclasses must implement this method.
        """
        raise NotImplementedError(
            f"{cls.__name__} must implement the register() method."
        )


# Mapping of feature names to module class paths
BUILTIN_MODULES: dict[str, str] = {
    "workflows": "artificer.workflows.module.WorkflowModule",
    "conversations": "artificer.conversations.module.ConversationModule",
}
