"""Loader module to dynamically load route.py files and validate router variable."""

import importlib.util
import sys
from pathlib import Path
from typing import Any


class RouterLoadError(Exception):
    """Exception raised when router loading fails."""
    pass


def load_router(route_file: Path) -> Any:
    """
    Dynamically load a route.py file and extract the router variable.

    Args:
        route_file: Path to the route.py file

    Returns:
        The router object (APIRouter instance)

    Raises:
        RouterLoadError: If the file cannot be loaded or router variable is missing
    """
    if not route_file.exists():
        raise RouterLoadError(f"Route file not found: {route_file}")

    if not route_file.is_file():
        raise RouterLoadError(f"Route path is not a file: {route_file}")

    # Generate a unique module name to avoid conflicts
    module_name = f"fextapi_route_{route_file.parent.name}_{id(route_file)}"

    try:
        # Load the module from file path
        spec = importlib.util.spec_from_file_location(module_name, route_file)

        if spec is None or spec.loader is None:
            raise RouterLoadError(f"Failed to load module spec: {route_file}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Check if router variable exists
        if not hasattr(module, "router"):
            raise RouterLoadError(
                f"Error: {route_file.relative_to(Path.cwd())} is missing 'router' definition"
            )

        router = getattr(module, "router")

        # Validate that router is an APIRouter instance
        from fastapi import APIRouter
        if not isinstance(router, APIRouter):
            raise RouterLoadError(
                f"Error: 'router' in {route_file.relative_to(Path.cwd())} "
                f"must be an APIRouter instance"
            )

        return router

    except RouterLoadError:
        # Re-raise our custom errors
        raise

    except Exception as e:
        # Catch all other exceptions (syntax errors, import errors, etc.)
        raise RouterLoadError(
            f"Error: Failed to load {route_file.relative_to(Path.cwd())}:\n{type(e).__name__}: {e}"
        ) from e
