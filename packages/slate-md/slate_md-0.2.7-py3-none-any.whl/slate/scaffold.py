"""Scaffolding module for creating new Slate sites.

This module handles the creation of the initial directory structure and
default files for a new Slate project. It provides the `create_scaffold`
function which sets up content, templates, and static asset directories.
"""

from datetime import datetime
from pathlib import Path

from rich.console import Console

console = Console()


def create_scaffold(target_dir: Path) -> None:
    """Creates a new Slate site structure at target_dir.

    Args:
        target_dir: The directory where the new site should be created.
    """

    if target_dir.exists() and any(target_dir.iterdir()):
        console.print(
            f"[bold red]Error:[/bold red] Directory {target_dir} is not empty."
        )
        return

    target_dir.mkdir(parents=True, exist_ok=True)

    # Create directories
    (target_dir / "content").mkdir()
    (target_dir / "content" / "blog").mkdir()
    (target_dir / "templates").mkdir()
    (target_dir / "static").mkdir()

    # Create files
    _create_index_md(target_dir / "content" / "index.md")
    _create_blog_md(target_dir / "content" / "blog" / "blog.md")
    _create_hello_world_md(target_dir / "content" / "blog" / "hello-world.md")
    _create_base_html(target_dir / "templates" / "base.html")
    _create_style_css(target_dir / "static" / "style.css")

    console.print(
        f"[bold green]Success![/bold green] Created new Slate site at [bold]{target_dir}[/bold]"
    )
    console.print(f"Run [bold]cd {target_dir} && slate build[/bold] to get started.")


def _create_index_md(path: Path) -> None:
    """Creates the default index.md file."""
    content = """---
title: Welcome to Slate
template: base.html
---

# Welcome to Slate

Slate is a static site generator designed for simplicity and flexibility.

## Features Showcase

### Formatting
You can use **bold**, *italic*, and ~~strikethrough~~ text.

### Lists
- Item 1
- Item 2
    - Nested Item A
    - Nested Item B

### Callouts
> [!NOTE]
> This is a note callout.

> [!WARNING]
> This is a warning callout.

### Code
```python
def hello():
    print("Hello, world!")
```

### Tables
| Feature | Status |
| :--- | :--- |
| Fast | Yes |
| Simple | Yes |

### Footnotes
Here is a footnote reference[^1].

[^1]: This is the footnote content.
"""
    path.write_text(content, encoding="utf-8")


def _create_blog_md(path: Path) -> None:
    """Creates the default blog.md category root file."""
    content = """---
title: Blog
template: base.html
---

# Blog

Here are my latest thoughts.

{{ blog_posts }}
"""
    path.write_text(content, encoding="utf-8")


def _create_hello_world_md(path: Path) -> None:
    """Creates a sample blog post."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    content = f"""---
title: Hello World
date: {date_str}
type: blog
template: base.html
author: Slate User
---

# Hello World

This is my first blog post using Slate!
"""
    path.write_text(content, encoding="utf-8")


def _create_base_html(path: Path) -> None:
    """Creates the default base HTML template."""
    content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <header>
        <nav>
            {{ nav_header }}
        </nav>
    </header>

    <main>
        {{ content }}
    </main>

    <footer>
        <p>Powered by Slate {{ version }}</p>
    </footer>
</body>
</html>
"""
    path.write_text(content, encoding="utf-8")


def _create_style_css(path: Path) -> None:
    """Creates the default CSS stylesheet."""
    content = """:root {
    --bg-color: #ffffff;
    --text-color: #333333;
    --primary-color: #007bff;
    --code-bg: #f4f4f4;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg-color: #1a1a1a;
        --text-color: #f0f0f0;
        --primary-color: #4da3ff;
        --code-bg: #2d2d2d;
    }
}

body {
    font-family: system-ui, -apple-system, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--bg-color);
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
}

header nav ul {
    list-style: none;
    padding: 0;
    display: flex;
    gap: 1rem;
}

a {
    color: var(--primary-color);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

pre {
    background: var(--code-bg);
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
}

blockquote {
    border-left: 4px solid var(--primary-color);
    margin: 0;
    padding-left: 1rem;
    color: #666;
}

.callout {
    padding: 1rem;
    border-radius: 4px;
    margin: 1rem 0;
}

.callout-note {
    background-color: rgba(0, 123, 255, 0.1);
    border-left: 4px solid #007bff;
}

.callout-warning {
    background-color: rgba(255, 193, 7, 0.1);
    border-left: 4px solid #ffc107;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
}

th, td {
    padding: 0.5rem;
    border: 1px solid #ddd;
}

th {
    background-color: var(--code-bg);
}
"""
    path.write_text(content, encoding="utf-8")
