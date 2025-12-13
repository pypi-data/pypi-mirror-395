"""CLI run command to start the development server."""

import sys
from pathlib import Path


def run_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = True) -> None:
    """
    Start the uvicorn development server.

    Args:
        host: Server host address
        port: Server port number
        reload: Enable auto-reload on file changes
    """
    # Check if app directory exists
    app_dir = Path.cwd() / "app"
    if not app_dir.exists():
        print("❌ Error: app directory not found, please run 'fextapi init' first")
        raise SystemExit(1)

    # Check if main.py exists
    main_py = app_dir / "main.py"
    if not main_py.exists():
        print("❌ Error: main.py file not found")
        raise SystemExit(1)

    print("🚀 Starting fextapi development server...\n")

    # Import and run uvicorn
    try:
        import uvicorn
    except ImportError:
        print("❌ Error: uvicorn not installed, please run 'pip install uvicorn[standard]'")
        raise SystemExit(1)

    # Add app directory to Python path so 'main' module can be imported
    sys.path.insert(0, str(app_dir))

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        reload_dirs=[str(app_dir)],
        log_level="info"
    )
