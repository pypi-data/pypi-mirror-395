"""Scanner module to discover route.py files in app directory."""

from pathlib import Path
from typing import Generator


class RouteInfo:
    """Information about a discovered route file."""

    def __init__(self, file_path: Path, api_path: str, is_dynamic: bool = False):
        """
        Initialize RouteInfo.

        Args:
            file_path: Absolute path to the route.py file
            api_path: API path (e.g., /products/{productid})
            is_dynamic: Whether the route contains dynamic parameters
        """
        self.file_path = file_path
        self.api_path = api_path
        self.is_dynamic = is_dynamic

    def __repr__(self) -> str:
        return f"RouteInfo(api_path='{self.api_path}', file_path='{self.file_path}')"


def scan_routes(app_root: Path, scan_dir: str | None = None) -> list[RouteInfo]:
    """
    Scan app directory and discover all route.py files.

    Args:
        app_root: Path to the app root directory
        scan_dir: Optional subdirectory to scan (e.g., "routers").
                  If provided, scans app_root/scan_dir but excludes scan_dir from API prefix.

    Returns:
        List of RouteInfo objects sorted by priority (static routes first)

    Raises:
        FileNotFoundError: If app_root doesn't exist
    """
    if not app_root.exists():
        raise FileNotFoundError(f"App directory not found: {app_root}")

    if not app_root.is_dir():
        raise NotADirectoryError(f"App path is not a directory: {app_root}")

    # Determine actual scan path and prefix base
    if scan_dir:
        scan_path = app_root / scan_dir
        if not scan_path.exists():
            raise FileNotFoundError(f"Scan directory not found: {scan_path}")
        if not scan_path.is_dir():
            raise NotADirectoryError(f"Scan path is not a directory: {scan_path}")
        # Use scan_path as the base for API path calculation (excludes scan_dir from prefix)
        prefix_base = scan_path
    else:
        scan_path = app_root
        prefix_base = app_root

    routes = list(_discover_routes(scan_path, prefix_base))

    # Sort routes: static routes first, then dynamic routes
    # This ensures /products/stats is matched before /products/{productid}
    routes.sort(key=lambda r: (r.is_dynamic, r.api_path))

    return routes


def _discover_routes(current_path: Path, app_root: Path) -> Generator[RouteInfo, None, None]:
    """
    Recursively discover route.py files.

    Args:
        current_path: Current directory being scanned
        app_root: Root app directory for path calculation

    Yields:
        RouteInfo objects for each discovered route
    """
    from fextapi.utils.path import build_api_path

    for item in current_path.iterdir():
        if item.is_file() and item.name == "route.py":
            # Build API path from directory structure
            api_path = build_api_path(item.parent, app_root)

            # Check if path contains dynamic parameters
            is_dynamic = "{" in api_path and "}" in api_path

            yield RouteInfo(
                file_path=item,
                api_path=api_path,
                is_dynamic=is_dynamic
            )

        elif item.is_dir() and not item.name.startswith((".", "__")):
            # Recursively scan subdirectories (exclude hidden and __pycache__)
            yield from _discover_routes(item, app_root)
