from pathlib import Path

# synchronize version with pyproject.toml file
from importlib.metadata import version
__version__ = version("markpub-themes")

def get_theme_path(theme_name="default"):
    """Get the path to a specific theme directory."""
    package_dir = Path(__file__).parent
    theme_path = package_dir / "themes" / theme_name
    if not theme_path.exists():
        raise ValueError(f"Theme '{theme_name}' not found")
    return str(theme_path)

def list_themes():
    """List all available themes."""
    themes_dir = Path(__file__).parent / "themes"
    return [d.name for d in themes_dir.iterdir() if d.is_dir() and not d.name.startswith('_')]

def get_theme_file(theme_name, file_path):
    """Get a specific file from a theme."""
    theme_path = Path(get_theme_path(theme_name))
    file_full_path = theme_path / file_path
    if not file_full_path.exists():
        raise FileNotFoundError(f"File '{file_path}' not found in theme '{theme_name}'")
    return str(file_full_path)

