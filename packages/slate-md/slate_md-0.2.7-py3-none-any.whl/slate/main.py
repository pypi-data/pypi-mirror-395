"""
This module provides the command-line interface (CLI) for the Slate tool.

Slate converts Markdown files into various static formats like HTML, Gemtext,
and Gophermap. This module handles:
- Argument parsing
- File loading
- Markdown parsing
- Rendering dispatch
- Output saving

It serves as the entry point for the application.
"""

import argparse
import importlib.metadata
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from markupsafe import Markup
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)
from rich.theme import Theme

from slate.frontmatter import (
    extract_frontmatter,
    merge_with_cli_args,
    validate_frontmatter,
)
from slate.loader import load_markdown, load_template
from slate.navigation import build_navigation_context
from slate.parse import generate_toc, parse_footnotes, parse_markdown_to_dicts
from slate.render import GemtextRenderer, GopherRenderer, HTMLRenderer

if TYPE_CHECKING:
    from slate.site import Page, Site

# Setup Rich Console with a custom theme for better visibility
custom_theme = Theme(
    {
        "info": "cyan",
        "warning": "yellow",
        "error": "bold red",
        "success": "bold green",
        "highlight": "magenta",
        "path": "blue underline",
    }
)
console = Console(theme=custom_theme, force_terminal=True)


def get_title(blocks: list[dict[str, Any]], override: str | None = None) -> str:
    """Determines the title of the document.

    Prioritizes the override title (from CLI or frontmatter), then looks for
    the first H1 or H2 heading in the parsed blocks. Defaults to "Untitled".

    Args:
        blocks: List of parsed Markdown blocks.
        override: Optional title override.

    Returns:
        The determined title string.
    """
    if override:
        return override
    for block in blocks:
        for heading_level in ("h1", "h2"):
            if heading_level in block:
                return block[heading_level]
    return "Untitled"


def save_text(text: str, output_path: str) -> None:
    """Saves the given text content to a specified output file.

    Ensures parent directories exist before writing.

    Args:
        text: The content to save.
        output_path: The destination file path.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def render_html(
    blocks: list[dict[str, Any]],
    args: argparse.Namespace,
    creation_date: str,
    creation_time: str,
    title: str,
    main_parser: argparse.ArgumentParser,
    version: str,
    source_path: str | None = None,
    modify_date: str | None = None,
    modify_time: str | None = None,
    footnotes: dict[str, str] | None = None,
) -> None:
    """Renders and saves the HTML output for a single page.

    Args:
        blocks: Parsed Markdown blocks.
        args: CLI arguments.
        creation_date: Date string.
        creation_time: Time string.
        title: Document title.
        main_parser: The argument parser (unused but kept for signature consistency).
        version: Slate version string.
        source_path: Path to the source Markdown file.
        modify_date: Modification date string.
        modify_time: Modification time string.
        footnotes: Dictionary of footnotes.
    """
    if not args.template:
        console.print(
            "[error]HTML output requires a Jinja2 template via -T/--template[/error]"
        )
        sys.exit(1)

    html_renderer = HTMLRenderer()

    # Render the content blocks to HTML
    content_html = html_renderer.render_blocks(
        blocks,
        title=title,
        description=(args.description or ""),
        creation_date=creation_date,
        creation_time=creation_time,
        modify_date=modify_date,
        modify_time=modify_time,
        version=version,
        footnotes=footnotes,
    )

    # Generate Table of Contents
    toc_html = generate_toc(blocks)

    # Load and render the Jinja2 template
    template = load_template(args.template)
    html_result = template.render(
        content=Markup(content_html),  # nosec B704
        title=title,
        description=(args.description or ""),
        creation_date=creation_date,
        creation_time=creation_time,
        modify_date=modify_date,
        modify_time=modify_time,
        version=version,
        toc=Markup(toc_html),  # nosec B704
    )

    # Append metadata comment if source path is provided (for debugging/tracking)
    if source_path and args.template:
        abs_source = Path(source_path).resolve()
        abs_template = Path(args.template).resolve()
        metadata = {
            "source": str(abs_source),
            "template": str(abs_template),
            "creation_date": creation_date,
            "creation_time": creation_time,
        }
        html_result += f"\n<!-- slate: {json.dumps(metadata)} -->"

    save_text(html_result, args.output)
    console.print(
        f"[success]HTML output saved at:[/success] [path]{args.output}[/path]"
    )


def render_gemtext(
    blocks: list[dict[str, Any]],
    args: argparse.Namespace,
    creation_date: str,
    creation_time: str,
    title: str,
    main_parser: argparse.ArgumentParser,
    version: str,
    modify_date: str | None = None,
    modify_time: str | None = None,
    footnotes: dict[str, str] | None = None,
    site: Any = None,
    page: Any = None,
) -> None:
    """Renders and saves the Gemtext output for a single page."""
    gemtext_renderer = GemtextRenderer()
    text_result = gemtext_renderer.render_blocks(
        blocks,
        title=title,
        description=(args.description or ""),
        creation_date=creation_date,
        creation_time=creation_time,
        modify_date=modify_date,
        modify_time=modify_time,
        version=version,
        footnotes=footnotes,
        site=site,
        page=page,
    )
    save_text(text_result, args.output)
    console.print(
        f"[success]GEMINI output saved at:[/success] [path]{args.output}[/path]"
    )


def render_gopher(
    blocks: list[dict[str, Any]],
    args: argparse.Namespace,
    creation_date: str,
    creation_time: str,
    title: str,
    main_parser: argparse.ArgumentParser,
    version: str,
    modify_date: str | None = None,
    modify_time: str | None = None,
    footnotes: dict[str, str] | None = None,
    site: Any = None,
    page: Any = None,
) -> None:
    """Renders and saves the Gopher output for a single page."""
    gopher_renderer = GopherRenderer()
    text_result = gopher_renderer.render_blocks(
        blocks,
        title=title,
        description=(args.description or ""),
        creation_date=creation_date,
        creation_time=creation_time,
        modify_date=modify_date,
        modify_time=modify_time,
        version=version,
        footnotes=footnotes,
        site=site,
        page=page,
    )
    save_text(text_result, args.output)
    console.print(
        f"[success]GOPHER output saved at:[/success] [path]{args.output}[/path]"
    )


def handle_page_build(
    args: argparse.Namespace, main_parser: argparse.ArgumentParser
) -> None:
    """Handles building a single page from a Markdown file.

    This function orchestrates the parsing, validation, and rendering of a single
    Markdown file into the requested format(s).
    """
    md_text = load_markdown(args.input)

    # Extract and process frontmatter and content
    frontmatter, content = extract_frontmatter(md_text)
    content, footnotes = parse_footnotes(content)

    # Validate frontmatter
    errors = validate_frontmatter(frontmatter, args.input)
    if errors:
        for error in errors:
            console.print(f"[error]{error}[/error]")
        sys.exit(1)

    # Merge CLI args with frontmatter (CLI takes precedence)
    cli_args_dict = {
        "title": args.title,
        "description": getattr(args, "description", None),
        "template": getattr(args, "template", None),
    }
    merged = merge_with_cli_args(frontmatter, cli_args_dict)

    if merged.get("title"):
        args.title = merged["title"]
    if merged.get("description"):
        args.description = merged["description"]
    if merged.get("template"):
        args.template = merged["template"]

    # Parse content into blocks
    blocks = parse_markdown_to_dicts(content)
    title = get_title(blocks, override=args.title)

    # Set dates
    now = datetime.now()
    creation_date = now.strftime("%d/%m/%Y")
    creation_time = now.strftime("%H:%M")
    modify_date = creation_date
    modify_time = creation_time

    try:
        version = f"v{importlib.metadata.version('slate-md')}"
    except importlib.metadata.PackageNotFoundError:
        version = "v0.0.0"

    # Determine format: CLI arg > Frontmatter > Default (html)
    fmt = args.format
    if not fmt and "format" in frontmatter:
        fmt = frontmatter["format"]
    if not fmt:
        fmt = "html"

    fmt = fmt.lower()

    # Dispatch to appropriate renderer
    if fmt == "html":
        render_html(
            blocks,
            args,
            creation_date,
            creation_time,
            title,
            main_parser,
            version,
            source_path=args.input,
            modify_date=modify_date,
            modify_time=modify_time,
            footnotes=footnotes,
        )
    elif fmt == "gemini":
        render_gemtext(
            blocks,
            args,
            creation_date,
            creation_time,
            title,
            main_parser,
            version,
            modify_date=modify_date,
            modify_time=modify_time,
            footnotes=footnotes,
        )
    elif fmt == "gopher":
        render_gopher(
            blocks,
            args,
            creation_date,
            creation_time,
            title,
            main_parser,
            version,
            modify_date=modify_date,
            modify_time=modify_time,
            footnotes=footnotes,
        )
    else:
        console.print(f"[error]Unsupported format: {fmt}[/error]")
        sys.exit(1)


def handle_site_build(
    args: argparse.Namespace, main_parser: argparse.ArgumentParser
) -> None:
    """Handles building the entire site from a directory.

    This function discovers the site structure, validates it, and then iterates
    through all pages to build them in the requested format(s).
    """
    from slate.site import discover_site, validate_site_structure

    # 1. Resolve Paths with Defaults
    project_root = Path(args.target).resolve()

    # Determine source directory (content/ or root)
    if (project_root / "content").is_dir():
        source_dir = project_root / "content"
    else:
        source_dir = project_root

    # Determine output directory
    if getattr(args, "output", None):
        output_dir = Path(args.output).resolve()
    else:
        output_dir = project_root

    # Determine templates directory
    if args.templates:
        templates_dir = Path(args.templates).resolve()
    elif (project_root / "templates").is_dir():
        templates_dir = (project_root / "templates").resolve()
    else:
        templates_dir = None

    structure = args.structure

    console.print(f"[info]Source:[/info] [path]{source_dir}[/path]")
    console.print(f"[info]Output:[/info] [path]{output_dir}[/path]")
    if templates_dir:
        console.print(f"[info]Templates:[/info] [path]{templates_dir}[/path]")

    # 2. Safe Clean with Backup
    if getattr(args, "clean", False):
        _clean_output_directory(output_dir, args.dry_run)

    # Discover and Validate Site
    try:
        site = discover_site(source_dir, output_dir, structure)
    except (FileNotFoundError, ValueError) as e:
        console.print(f"[error]{e}[/error]")
        sys.exit(1)

    warnings = validate_site_structure(site)
    if warnings:
        for warning in warnings:
            console.print(f"[warning]{warning}[/warning]")

    console.print(f"Found [highlight]{len(site.categories)}[/highlight] categories")

    try:
        version = f"v{importlib.metadata.version('slate-md')}"
    except importlib.metadata.PackageNotFoundError:
        version = "v0.0.0"

    # Collect all pages to build
    all_pages: list[tuple[Any, str | None]] = []
    # Index
    all_pages.append((site.index_page, None))  # (Page, CategoryName)
    # Categories
    for cat_name, category in site.categories.items():
        all_pages.append((category.root_page, cat_name))
        for page in category.pages:
            all_pages.append((page, cat_name))

    total_pages = len(all_pages)

    # 3. Build Loop with Progress Bar
    formats = getattr(args, "formats_list", ["html"])

    for fmt in formats:
        fmt_dir_name = "gemini" if fmt in ("gemini", "gemtext") else fmt

        # Determine output root for this format
        # If multiple formats, enforce subdirectories: output_dir / fmt
        if len(formats) > 1:
            current_output_dir = output_dir / fmt_dir_name
        else:
            current_output_dir = output_dir

        console.print(f"[bold]Building {fmt.upper()} to {current_output_dir}...[/bold]")
        current_output_dir.mkdir(parents=True, exist_ok=True)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task(f"[cyan]Building {fmt} site...", total=total_pages)

            for page, category_name in all_pages:
                if args.dry_run:
                    console.print(
                        f"[info]Would build [bold]{page.title}[/bold] ({fmt})...[/info]"
                    )
                    progress.advance(task)
                else:
                    progress.update(
                        task,
                        description=f"Building [bold]{page.title}[/bold] ({fmt})...",
                    )
                    _rebuild_page(
                        page,
                        site,
                        category_name,
                        version,
                        main_parser,
                        templates_dir,
                        fmt=fmt,
                        output_root=current_output_dir,
                        project_root=output_dir,
                    )
                    progress.advance(task)

            # Generate RSS Feeds (currently HTML only)
            if fmt == "html":
                _generate_rss_feeds(
                    site, current_output_dir, structure, args.dry_run, progress, task
                )

    console.print(
        f"\n[success]✓ Site build complete![/success] Built [highlight]{total_pages}[/highlight] pages across {len(formats)} formats."
    )


def _clean_output_directory(output_dir: Path, dry_run: bool) -> None:
    """Safely cleans the output directory by backing up files before deletion."""
    if dry_run:
        console.print("[highlight][DRY RUN] Cleaning output directory...[/highlight]")
    else:
        console.print("[highlight]Cleaning output directory...[/highlight]")

    # Identify files to clean: index.html in root, and everything in pages/
    files_to_clean = []

    # Root index.html
    root_index = output_dir / "index.html"
    if root_index.exists() and root_index.is_file():
        files_to_clean.append(root_index)

    # Pages directory
    pages_dir = output_dir / "pages"
    if pages_dir.exists() and pages_dir.is_dir():
        for p in pages_dir.rglob("*"):
            if p.is_file():
                files_to_clean.append(p)

    if files_to_clean:
        if dry_run:
            console.print(
                f"[info]Would backup and delete {len(files_to_clean)} files:[/info]"
            )
            for f in files_to_clean:
                console.print(f"  - {f.relative_to(output_dir)}")
        else:
            # Create backup
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_dir = output_dir / "backups" / timestamp
            backup_dir.mkdir(parents=True, exist_ok=True)

            console.print(
                f"Backing up {len(files_to_clean)} files to [path]{backup_dir}[/path]..."
            )

            for file_path in files_to_clean:
                # Calculate relative path to preserve structure in backup
                try:
                    rel_path = file_path.relative_to(output_dir)
                except ValueError:
                    rel_path = Path(file_path.name)

                backup_dest = backup_dir / rel_path
                backup_dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, backup_dest)

                # Delete original
                file_path.unlink()

            # Clean up empty directories in pages/
            if pages_dir.exists():
                # Walk bottom-up to remove empty dirs
                for p in sorted(
                    pages_dir.rglob("*"), key=lambda x: len(x.parts), reverse=True
                ):
                    if p.is_dir() and not any(p.iterdir()):
                        p.rmdir()
                # Remove pages/ itself if empty
                if not any(pages_dir.iterdir()):
                    pages_dir.rmdir()

            console.print(
                f"[success]Clean complete.[/success] Removed {len(files_to_clean)} files."
            )
    else:
        console.print("[info]Nothing to clean.[/info]")


def _generate_rss_feeds(
    site: "Site",
    output_dir: Path,
    structure: str,
    dry_run: bool,
    progress: Progress,
    task: Any,
) -> None:
    """Generates RSS feeds for categories with blog posts."""
    for cat_name, category in site.categories.items():
        if category.blog_posts:
            if dry_run:
                console.print(
                    f"[info]Would generate RSS for [bold]{cat_name}[/bold]...[/info]"
                )
            else:
                progress.update(
                    task,
                    description=f"Generating RSS for [bold]{cat_name}[/bold]...",
                )
                from slate.rss import generate_rss_feed

                site_url = site.index_page.frontmatter.get("url", "https://example.com")
                site_title = site.index_page.title
                site_desc = site.index_page.frontmatter.get("description", "")

                feed_xml = generate_rss_feed(category, site_url, site_title, site_desc)

                if structure == "tree":
                    feed_path = output_dir / "pages" / cat_name / "feed.xml"
                else:
                    feed_path = output_dir / cat_name / "feed.xml"

                feed_path.parent.mkdir(parents=True, exist_ok=True)
                feed_path.write_text(feed_xml, encoding="utf-8")


def _rebuild_page(
    page: "Page",
    site: "Site",
    category_name: str | None,
    version: str,
    main_parser: argparse.ArgumentParser,
    templates_dir: Path | None = None,
    fmt: str = "html",
    output_root: Path | None = None,
    project_root: Path | None = None,
) -> None:
    """Helper to rebuild a single page within a site build.

    Args:
        page: The Page object to rebuild.
        site: The Site object.
        category_name: The category name (if any).
        version: Slate version string.
        main_parser: Argument parser.
        templates_dir: Path to templates directory.
        fmt: Output format.
        output_root: Root directory for output (for multi-format builds).
        project_root: Original project root (for calculating relative paths).
    """
    md_text = page.source_path.read_text(encoding="utf-8")

    frontmatter, content = extract_frontmatter(md_text)
    content, footnotes = parse_footnotes(content)

    blocks = parse_markdown_to_dicts(content)
    title = page.title
    nav_context = build_navigation_context(site, category_name, page)

    now = datetime.now()
    modify_date = now.strftime("%d/%m/%Y")
    modify_time = now.strftime("%H:%M")

    creation_date = (
        str(frontmatter.get("date", modify_date))
        if "date" in frontmatter
        else modify_date
    )
    creation_time = modify_time

    # Determine output path based on output_root and format
    if output_root:
        # Calculate relative path from project root to preserve structure
        rel_path = Path(page.output_path.name)  # Fallback

        if project_root:
            try:
                rel_path = page.output_path.relative_to(project_root)
            except ValueError:
                rel_path = Path(page.output_path.name)

        # Change extension based on format
        suffix = (
            ".html"
            if fmt == "html"
            else ".gmi"
            if fmt in ("gemini", "gemtext")
            else ".txt"
        )
        rel_path = rel_path.with_suffix(suffix)

        final_output_path = output_root / rel_path
    else:
        # Single format legacy: use page's pre-calculated output path
        final_output_path = page.output_path

    template_path_str = frontmatter.get("template")
    if fmt == "html" and not template_path_str:
        return

    # Create a lightweight args object for the renderers
    args = argparse.Namespace(
        template=str(template_path_str) if template_path_str else None,
        description=frontmatter.get("description", ""),
        output=str(final_output_path),
    )

    if fmt == "html":
        # HTML Rendering
        template_path = Path(args.template)
        if templates_dir and not template_path.is_absolute():
            potential_path = templates_dir / template_path
            if potential_path.exists():
                template_path = potential_path
        args.template = str(template_path)

        html_renderer = HTMLRenderer()
        toc_html = generate_toc(blocks)

        context = {
            "title": title,
            "description": args.description,
            "creation_date": creation_date,
            "creation_time": creation_time,
            "modify_date": modify_date,
            "modify_time": modify_time,
            "version": version,
            "toc": Markup(toc_html),  # nosec B704
            **nav_context,
        }

        content_html = html_renderer.render_blocks(
            blocks,
            title=title,
            description=args.description,
            creation_date=creation_date,
            creation_time=creation_time,
            modify_date=modify_date,
            modify_time=modify_time,
            version=version,
            site=site,
            page=page,
            toc=toc_html,
            footnotes=footnotes,
        )

        # Replace navigation variables in content
        for var_name, var_value in nav_context.items():
            content_html = content_html.replace(f"{{{{{var_name}}}}}", var_value)

        try:
            template = load_template(args.template)
            final_html = template.render(content=Markup(content_html), **context)  # nosec B704
        except FileNotFoundError:
            console.print(f"[error]Template not found: {args.template}[/error]")
            return

        # Append metadata comment
        metadata = {
            "source": str(page.source_path.resolve()),
            "template": str(Path(args.template).resolve()),
            "creation_date": creation_date,
            "creation_time": creation_time,
        }
        metadata_comment = f"<!-- slate: {json.dumps(metadata)} -->"
        final_html = final_html.rstrip() + "\n" + metadata_comment + "\n"

        final_output_path.parent.mkdir(parents=True, exist_ok=True)
        save_text(final_html, str(final_output_path))

    elif fmt in ("gemini", "gemtext"):
        render_gemtext(
            blocks,
            args,
            creation_date,
            creation_time,
            title,
            main_parser,
            version,
            modify_date=modify_date,
            modify_time=modify_time,
            footnotes=footnotes,
            site=site,
            page=page,
        )
    elif fmt == "gopher":
        render_gopher(
            blocks,
            args,
            creation_date,
            creation_time,
            title,
            main_parser,
            version,
            modify_time=modify_time,
            footnotes=footnotes,
            site=site,
            page=page,
        )


def handle_unified_build(
    args: argparse.Namespace, main_parser: argparse.ArgumentParser
) -> None:
    """Handles the unified `build` command (site or page).

    Dispatches to `handle_site_build` or `handle_page_build` based on the target.
    """
    target = Path(args.target).resolve()

    # Determine formats
    formats = []
    if args.formats:
        formats = [f.strip().lower() for f in args.formats.split(",") if f.strip()]
    elif args.format:
        formats = [args.format.lower()]
    else:
        formats = ["html"]

    # Validate formats
    valid_formats = {"html", "gemini", "gopher", "gemtext"}
    for f in formats:
        if f not in valid_formats:
            console.print(f"[error]Unsupported format: {f}[/error]")
            sys.exit(1)

    # Store processed formats back in args for downstream use
    args.formats_list = formats

    if target.is_dir():
        # Site Build
        handle_site_build(args, main_parser)
    elif target.is_file():
        # Page Build
        args.input = str(target)
        base_output = args.output

        for fmt in formats:
            # Set the current format for this iteration
            args.format = fmt

            # Determine output path for this format
            if len(formats) > 1:
                # Enforce monorepo structure: output_dir/format/filename
                output_root = Path(base_output) if base_output else target.parent
                fmt_dir_name = "gemini" if fmt in ("gemini", "gemtext") else fmt

                # Create format-specific subdirectory
                current_output_dir = output_root / fmt_dir_name
                current_output_dir.mkdir(parents=True, exist_ok=True)

                # Calculate filename
                suffix = (
                    ".html"
                    if fmt == "html"
                    else ".gmi"
                    if fmt in ("gemini", "gemtext")
                    else ".txt"
                )

                # If target is a file, use its stem
                filename = target.with_suffix(suffix).name
                args.output = str(current_output_dir / filename)

            else:
                if not base_output:
                    suffix = (
                        ".html"
                        if fmt == "html"
                        else ".gmi"
                        if fmt in ("gemini", "gemtext")
                        else ".txt"
                    )
                    args.output = str(target.with_suffix(suffix))
                else:
                    args.output = base_output

            handle_page_build(args, main_parser)

    else:
        console.print(f"[error]Target '{target}' not found.[/error]")
        sys.exit(1)


def handle_rerun_last(
    args: argparse.Namespace, main_parser: argparse.ArgumentParser
) -> None:
    """Handles the `rebuild` subcommand (re-run last)."""
    last_run_file = Path("slate.json")
    if not last_run_file.exists():
        console.print(
            "[error]No previous run found. Run 'slate build' or 'slate draft' first.[/error]"
        )
        sys.exit(1)

    try:
        saved_args = json.loads(last_run_file.read_text())
        cmd_args = saved_args.get("args", [])
        console.print(f"[info]Re-running:[/info] slate {' '.join(cmd_args)}")

        # Prevent infinite recursion if slate.json contains 'rebuild'
        if cmd_args and cmd_args[0] == "rebuild":
            console.print("[error]Cannot rebuild a rebuild command.[/error]")
            sys.exit(1)

        new_args = main_parser.parse_args(cmd_args)
        if hasattr(new_args, "func"):
            new_args.func(new_args, main_parser)

    except Exception as e:
        console.print(f"[error]Failed to re-run last command: {e}[/error]")
        sys.exit(1)


def handle_draft(
    args: argparse.Namespace, main_parser: argparse.ArgumentParser
) -> None:
    """Handles the `draft` subcommand."""
    from slate.scaffold import create_scaffold

    target_path = Path(args.name).resolve()
    create_scaffold(target_path)


def main(args_list: list[str] | None = None) -> None:
    """Main entry point for the Slate command-line interface."""
    main_parser = argparse.ArgumentParser(
        description="slate — Markdown to static formats (HTML/Gemini/Gopher)"
    )

    # Add version flag
    main_parser.add_argument(
        "-v", "--version", action="store_true", help="Show version and exit"
    )

    subparsers = main_parser.add_subparsers(dest="command", help="Sub-command help")

    # Draft command
    parser_draft = subparsers.add_parser("draft", help="Create a new Slate project")
    parser_draft.add_argument("name", help="Name of the new site (directory)")
    parser_draft.set_defaults(func=handle_draft)

    # Build command (Unified)
    parser_build = subparsers.add_parser("build", help="Build site or single page")
    parser_build.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target directory (site) or file (page) to build",
    )
    parser_build.add_argument(
        "-o", "--output", dest="output", help="Output directory or file"
    )
    parser_build.add_argument(
        "-T",
        "--templates",  # For site
        dest="templates",
        help="Templates directory (default: templates/)",
    )
    parser_build.add_argument(
        "--template",  # For page
        dest="template",
        help="Jinja2 template path (for single page)",
    )
    parser_build.add_argument(
        "--structure",
        dest="structure",
        choices=("flat", "tree"),
        default="tree",
        help="Output structure (default: tree)",
    )
    parser_build.add_argument(
        "--clean",
        action="store_true",
        help="Safely clean output directory before building",
    )
    parser_build.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate actions without making changes",
    )
    parser_build.add_argument(
        "-f",
        "--format",
        dest="format",
        help="Output format (single). Legacy option.",
    )
    parser_build.add_argument(
        "--formats",
        dest="formats",
        help="Comma-separated list of output formats (e.g. html,gemini,gopher). Overrides -f.",
    )
    parser_build.add_argument(
        "--ipfs",
        action="store_true",
        help="Enable IPFS compatibility (forces relative links).",
    )
    # Page specific args (optional)
    parser_build.add_argument("-t", "--title", dest="title", help="Title override")
    parser_build.add_argument(
        "-d", "--description", dest="description", help="Brief description"
    )

    parser_build.set_defaults(func=handle_unified_build)

    # Rebuild command
    parser_rebuild = subparsers.add_parser("rebuild", help="Re-run the last command")
    parser_rebuild.set_defaults(func=handle_rerun_last)

    try:
        args = main_parser.parse_args(args_list)

        # Handle Version Flag
        if args.version:
            try:
                v = importlib.metadata.version("slate-md")
                console.print(f"slate-md [bold cyan]v{v}[/bold cyan]")
            except importlib.metadata.PackageNotFoundError:
                console.print("slate-md [bold red]unknown version[/bold red]")
            sys.exit(0)

        if not args.command:
            main_parser.print_help()
            sys.exit(0)

        if args.command != "rebuild":
            try:
                raw_args = args_list if args_list is not None else sys.argv[1:]
                Path("slate.json").write_text(json.dumps({"args": raw_args}, indent=4))
            except Exception as e:
                console.print(
                    f"[warning]Warning: Failed to save run state: {e}[/warning]"
                )

        if hasattr(args, "func"):
            args.func(args, main_parser)
    except Exception as e:
        console.print(f"[error]Error: {e}[/error]")
        sys.exit(1)


if __name__ == "__main__":
    main()
