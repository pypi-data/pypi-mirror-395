"""
This module handles loading content from files, such as Markdown documents
and Jinja2 HTML templates. It provides utilities to read file contents
and prepare templating environments.
"""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template


def load_markdown(md_path: str | Path) -> str:
    """Loads content from a Markdown file.

    Args:
        md_path: The file path to the Markdown document.

    Returns:
        The content of the Markdown file as a string.
    """
    path = Path(md_path)
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as err:
        raise FileNotFoundError(f"Input file '{path}' not found.") from err
    except PermissionError as err:
        raise PermissionError(f"Permission denied accessing '{path}'.") from err


def load_template(template_path: str | Path) -> Template:
    """Loads a Jinja2 template from the specified path.

    Args:
        template_path: The file path to the Jinja2 template.

    Returns:
        A Jinja2 Template object ready for rendering.
    """
    path = Path(template_path)
    if not path.exists():
        raise FileNotFoundError(f"Template file '{path}' not found.")

    # FileSystemLoader needs a string or Path object (Jinja2 supports Path)
    env = Environment(loader=FileSystemLoader(path.parent), autoescape=True)
    return env.get_template(path.name)
