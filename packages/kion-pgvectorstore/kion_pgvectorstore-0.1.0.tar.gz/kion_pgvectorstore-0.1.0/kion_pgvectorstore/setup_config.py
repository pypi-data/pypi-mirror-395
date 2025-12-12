import os
import shutil

try:
    # Python 3.9+ recommended API
    from importlib.resources import files as resource_files
except Exception:
    # Fallback for older Python: pip install importlib_resources
    from importlib_resources import files as resource_files  # type: ignore

PACKAGE_NAME = "kion_pgvectorstore"

def _copy_from_package(resource_name: str, destination_path: str, force: bool) -> None:
    """
    Copy a single resource from the installed package to a destination path.

    Args:
        resource_name: File name inside the package (relative to the package root).
        destination_path: Full path on disk to copy to.
        force: If True, overwrite an existing file.
    """
    # If the file exists and we are not forcing overwrite, skip but do not abort the rest.
    if os.path.exists(destination_path) and not force:
        print(f"- Skipping '{os.path.basename(destination_path)}': already exists. Use --force to overwrite.")
        return

    try:
        src = resource_files(PACKAGE_NAME).joinpath(resource_name)
        if not src.exists():
            raise FileNotFoundError(f"Resource '{resource_name}' not found in package '{PACKAGE_NAME}'.")
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(destination_path) or ".", exist_ok=True)
        shutil.copy2(src, destination_path)
        if force and os.path.exists(destination_path):
            print(f"- Successfully overwrote '{os.path.basename(destination_path)}'.")
        else:
            print(f"- Successfully created '{os.path.basename(destination_path)}'.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Ensure the file is included as package data in your packaging configuration (pyproject.toml or setup.py).")
    except Exception as e:
        print(f"An unexpected error occurred copying '{resource_name}': {e}")

def create_env_file(destination_dir: str | None = None, force: bool = False) -> None:
    """
    Create starter files (.env, dotenv_finder.py, app.py) in the chosen directory.

    Args:
        destination_dir: Directory to write files to. Defaults to the current working directory.
        force: If True, overwrites existing files. Defaults to False.
    """
    if destination_dir is None:
        destination_dir = os.getcwd()

    destination_dir = os.path.abspath(destination_dir)
    os.makedirs(destination_dir, exist_ok=True)

    print(f"Initializing files in: {destination_dir}")

    # Define filenames expected to exist inside the installed package
    # Note: packaging dotfiles (like '.env') can be tricky. If you prefer,
    # ship 'env.template' in your package and copy it to '.env' here.
    targets = [
        # (resource in package, destination filename on disk)
        (".env", ".env"),
        ("app.py", "app.py"),
        ("README.md", "README.md")
    ]

    for resource_name, dest_name in targets:
        dest_path = os.path.join(destination_dir, dest_name)
        # Try the direct resource name first
        _copy_from_package(resource_name, dest_path, force=force)
        # Optional fallback: if the resource was '.env' and not found, try 'env.template'
        if resource_name == ".env" and not os.path.exists(dest_path):
            _copy_from_package("env.template", dest_path, force=force)
