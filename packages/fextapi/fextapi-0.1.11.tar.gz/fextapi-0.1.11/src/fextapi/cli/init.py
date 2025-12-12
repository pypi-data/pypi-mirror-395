"""CLI init command to initialize a new fextapi project."""

import shutil
from pathlib import Path


def init_project(target_dir: Path = None) -> None:
    """
    Initialize a new fextapi project in the target directory.

    Args:
        target_dir: Target directory for the project (default: current directory)
    """
    if target_dir is None:
        target_dir = Path.cwd()

    # Get templates directory
    templates_dir = Path(__file__).parent / "templates"

    # Create app directory structure
    app_dir = target_dir / "app"
    api_dir = app_dir / "api"
    api_dir.mkdir(parents=True, exist_ok=True)

    # Create components directory
    components_dir = app_dir / "components"
    components_dir.mkdir(parents=True, exist_ok=True)

    # Prepare files to copy
    files_to_copy = [
        (templates_dir / "main.py.template", app_dir / "main.py"),
        (templates_dir / "route.py.template", api_dir / "route.py"),
        (templates_dir / "README.md.template", target_dir / "README.md"),
    ]

    # Only copy pyproject.toml if it doesn't exist
    pyproject_path = target_dir / "pyproject.toml"
    if not pyproject_path.exists():
        files_to_copy.append(
            (templates_dir / "pyproject.toml.template", pyproject_path)
        )
    else:
        print("⚠️  pyproject.toml already exists, skipping...")

    for src, dest in files_to_copy:
        if not src.exists():
            print(f"⚠️  Warning: Template file not found: {src}")
            continue

        shutil.copy2(src, dest)
        print(f"✓ Created: {dest.relative_to(target_dir)}")

    print("\n✅ Project initialized successfully!")
    print("\nNext steps:")
    print("  1. Run 'fextapi run' to start development server")
    print("  2. Visit http://127.0.0.1:8000/docs to view API documentation")
