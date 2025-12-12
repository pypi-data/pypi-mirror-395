"""Registry module to register routes to FastAPI app."""

from pathlib import Path

from fastapi import FastAPI

from fextapi.router.loader import RouterLoadError, load_router
from fextapi.router.scanner import scan_routes


def init(app: FastAPI, app_root: Path | str = "app", scan_dir: str | None = None) -> None:
    """
    Initialize fextapi by scanning and registering all routes to the FastAPI app.

    Args:
        app: FastAPI application instance
        app_root: Path to the app root directory (default: "app")
        scan_dir: Optional subdirectory to scan (e.g., "routers").
                  If provided, scans app_root/scan_dir but excludes scan_dir from API prefix.

    Raises:
        FileNotFoundError: If app_root doesn't exist
        RouterLoadError: If any route file has errors
    """
    # Convert to Path object
    if isinstance(app_root, str):
        app_root = Path(app_root)

    # Make it absolute
    if not app_root.is_absolute():
        app_root = Path.cwd() / app_root

    # Scan for routes
    routes = scan_routes(app_root, scan_dir)

    if not routes:
        print(f"⚠️  Warning: No route.py files found in {app_root}")
        return

    # Load and register each route
    registered_count = 0
    print("\n⚛️  Starting route registration...")
    for route_info in routes:
        try:
            router = load_router(route_info.file_path)

            # Register router to FastAPI app
            app.include_router(router, prefix=route_info.api_path)

            registered_count += 1
            print(f"\t✓ Registered route: {route_info.api_path}")

        except RouterLoadError as e:
            # Fast fail: stop on first error
            print(f"\n❌ {e}")
            raise SystemExit(1) from e

    print(f"✅ Successfully registered {registered_count} route(s)\n")
