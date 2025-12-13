"""Module discovery and loading."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

from artificer.cli.module import ArtificerModule, BUILTIN_MODULES

if TYPE_CHECKING:
    pass


def import_builtin_module(feature: str) -> type[ArtificerModule]:
    """Import a built-in module by feature name.

    Args:
        feature: The feature name (e.g., "workflows").

    Returns:
        The module class.

    Raises:
        RuntimeError: If feature is unknown or module cannot be imported.
    """
    if feature not in BUILTIN_MODULES:
        available = ", ".join(sorted(BUILTIN_MODULES.keys()))
        raise RuntimeError(
            f"Unknown feature '{feature}'. Available features: {available}"
        )

    module_path = BUILTIN_MODULES[feature]

    # Split into module path and class name
    module_name, class_name = module_path.rsplit(".", 1)

    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        raise RuntimeError(
            f"Failed to import module for feature '{feature}': {e}. "
            f"Is the package installed?"
        ) from e

    try:
        module_class = getattr(module, class_name)
    except AttributeError as e:
        raise RuntimeError(
            f"Module '{module_name}' does not have class '{class_name}'."
        ) from e

    if not isinstance(module_class, type) or not issubclass(module_class, ArtificerModule):
        raise RuntimeError(
            f"'{module_path}' is not a subclass of ArtificerModule."
        )

    return module_class


def load_custom_modules(entrypoint: str) -> list[type[ArtificerModule]]:
    """Load custom modules from an entrypoint module.

    Args:
        entrypoint: Dotted import path to the entrypoint module.

    Returns:
        List of discovered ArtificerModule subclasses.

    Raises:
        RuntimeError: If entrypoint cannot be imported.
    """
    try:
        module = importlib.import_module(entrypoint)
    except ImportError as e:
        raise RuntimeError(
            f"Failed to import entrypoint '{entrypoint}': {e}"
        ) from e

    modules: list[type[ArtificerModule]] = []

    for name in dir(module):
        obj = getattr(module, name)
        # Check if it's a class, is a subclass of ArtificerModule,
        # and is not the base class itself
        if (
            isinstance(obj, type)
            and issubclass(obj, ArtificerModule)
            and obj is not ArtificerModule
        ):
            modules.append(obj)

    return modules
