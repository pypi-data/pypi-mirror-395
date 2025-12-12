"""Site structure discovery and validation for Slate.

This module handles discovering the structure of a multi-page site,
building a graph of categories and pages starting from index.md.

Site Structure Rules:
- index.md is the entry point (defines categories in frontmatter)
- Each category requires {category}.md root page
- Pages in {category}/ directory belong to that category
- Strict 1:1 category membership
- Blog posts (type: blog) require explicit date field
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from slate.frontmatter import extract_frontmatter, validate_frontmatter


@dataclass
class Page:
    """Represents a single page in the site."""

    source_path: Path  # Path to .md file
    output_path: Path  # Path to output file (.html, .gmi, etc.)
    frontmatter: dict[str, Any]  # Parsed frontmatter
    category: str | None  # Category name or None for index
    is_category_root: bool  # True if this is {category}.md
    content: str = ""  # Markdown content (without frontmatter)

    @property
    def title(self) -> str:
        """Get page title from frontmatter or filename."""
        return self.frontmatter.get(
            "title", self.source_path.stem.replace("-", " ").title()
        )

    @property
    def is_blog_post(self) -> bool:
        """Check if this page is a blog post."""
        return self.frontmatter.get("type") == "blog"


@dataclass
class Category:
    """Represents a category with its pages."""

    name: str  # Category name (e.g., "blog")
    root_page: Page  # The {category}.md page
    pages: list[Page] = field(default_factory=list)  # Pages in this category

    @property
    def blog_posts(self) -> list[Page]:
        """Get only blog posts in this category, sorted by date (newest first)."""
        posts = [p for p in self.pages if p.is_blog_post]
        # Sort by date if available
        posts.sort(key=lambda p: p.frontmatter.get("date", "0000-00-00"), reverse=True)
        return posts


@dataclass
class Site:
    """Represents the entire site structure."""

    root_path: Path  # Root directory of the site
    index_page: Page  # The index.md page
    categories: dict[str, Category] = field(
        default_factory=dict
    )  # Category name → Category
    orphaned_pages: list[Page] = field(
        default_factory=list
    )  # Pages not in any category


def discover_site(
    root_path: Path, output_path: Path | None = None, structure: str = "flat"
) -> Site:
    """Discover site structure starting from root_path.

    Algorithm:
    1. Find and parse index.md
    2. Read categories list from index.md frontmatter
    3. For each category, find {category}.md root page
    4. Scan {category}/ directory for all .md files
    5. Build Site object with full structure

    Args:
        root_path: Root directory containing index.md (source)
        output_path: Root directory for output files (default: same as root_path)
        structure: Output structure ("flat" or "tree")

    Returns:
        Site object representing the discovered structure

    Raises:
        FileNotFoundError: If index.md is missing
        ValueError: If site structure is invalid
    """
    root_path = Path(root_path).resolve()
    output_root = Path(output_path).resolve() if output_path else root_path

    # Step 1: Find and parse index.md
    index_path = root_path / "index.md"
    if not index_path.exists():
        raise FileNotFoundError(
            f"Site root must contain index.md. Not found at: {index_path}"
        )

    index_content = index_path.read_text(encoding="utf-8")
    index_frontmatter, index_md = extract_frontmatter(index_content)

    # Validate index frontmatter
    errors = validate_frontmatter(index_frontmatter, str(index_path))
    if errors:
        raise ValueError("Invalid index.md frontmatter:\n" + "\n".join(errors))

    index_page = Page(
        source_path=index_path,
        output_path=output_root / "index.html",
        frontmatter=index_frontmatter,
        category=None,
        is_category_root=False,
        content=index_md,
    )

    # Step 2: Read categories from index frontmatter
    category_names = index_frontmatter.get("categories", [])
    if not isinstance(category_names, list):
        raise ValueError(
            "index.md frontmatter 'categories' must be a list, "
            f"got: {type(category_names).__name__}"
        )

    site = Site(
        root_path=root_path,
        index_page=index_page,
        categories={},
        orphaned_pages=[],
    )

    # Step 3 & 4: Process each category
    for category_name in category_names:
        if not isinstance(category_name, str):
            raise ValueError(f"Category name must be string, got: {category_name}")

        category = _discover_category(root_path, category_name, output_root, structure)
        site.categories[category_name] = category

    # Find orphaned pages (optional - for now we don't scan for them)
    # This would involve scanning all .md files and checking if they're in any category

    return site


def _discover_category(
    root_path: Path, category_name: str, output_root: Path, structure: str
) -> Category:
    """Discover a single category's structure.

    Args:
        root_path: Site root directory (source)
        category_name: Name of the category (e.g., "blog")
        output_root: Root directory for output
        structure: Output structure ("flat" or "tree")

    Returns:
        Category object with root page and all pages

    Raises:
        FileNotFoundError: If category root page is missing
        ValueError: If category structure is invalid
    """
    # Find category root page ({category}.md)
    root_page_path = root_path / f"{category_name}.md"
    if not root_page_path.exists():
        raise FileNotFoundError(
            f"Category '{category_name}' requires root page at: {root_page_path}"
        )

    # Parse category root page
    root_content = root_page_path.read_text(encoding="utf-8")
    root_frontmatter, root_md = extract_frontmatter(root_content)

    errors = validate_frontmatter(root_frontmatter, str(root_page_path))
    if errors:
        raise ValueError(
            f"Invalid {category_name}.md frontmatter:\n" + "\n".join(errors)
        )

    # Calculate output path based on structure
    if structure == "tree":
        # pages/category.html
        output_path = output_root / "pages" / f"{category_name}.html"
    else:
        # category.html
        output_path = output_root / f"{category_name}.html"

    root_page = Page(
        source_path=root_page_path,
        output_path=output_path,
        frontmatter=root_frontmatter,
        category=category_name,
        is_category_root=True,
        content=root_md,
    )

    category = Category(name=category_name, root_page=root_page, pages=[])

    # Scan {category}/ directory for pages
    category_dir = root_path / category_name
    if category_dir.exists() and category_dir.is_dir():
        for md_file in category_dir.glob("*.md"):
            page = _parse_page(
                md_file, category_name, root_path, output_root, structure
            )
            category.pages.append(page)

    return category


def _parse_page(
    md_path: Path,
    category_name: str,
    root_path: Path,
    output_root: Path,
    structure: str,
) -> Page:
    """Parse a single Markdown file into a Page object.

    Args:
        md_path: Path to the .md file
        category_name: Category this page belongs to
        root_path: Site root directory (source)
        output_root: Root directory for output
        structure: Output structure ("flat" or "tree")

    Returns:
        Page object

    Raises:
        ValueError: If frontmatter is invalid
    """
    content = md_path.read_text(encoding="utf-8")
    frontmatter, md = extract_frontmatter(content)

    errors = validate_frontmatter(frontmatter, str(md_path))
    if errors:
        raise ValueError(f"Invalid {md_path}:\n" + "\n".join(errors))

    # Validate category matches if specified in frontmatter
    if "category" in frontmatter and frontmatter["category"] != category_name:
        raise ValueError(
            f"{md_path}: Frontmatter category '{frontmatter['category']}' "
            f"doesn't match directory category '{category_name}'"
        )

    # Build output path
    relative_path = md_path.relative_to(root_path)

    if structure == "tree":
        # pages/category/page.html
        # We prepend "pages/" to the relative path
        output_path = output_root / "pages" / relative_path.with_suffix(".html")
    else:
        # category/page.html (mirrors source)
        output_path = output_root / relative_path.with_suffix(".html")

    return Page(
        source_path=md_path,
        output_path=output_path,
        frontmatter=frontmatter,
        category=category_name,
        is_category_root=False,
        content=md,
    )


def validate_site_structure(site: Site) -> list[str]:
    """Validate site structure and return list of warnings/errors.

    Checks:
    - All categories have root pages (checked during discovery)
    - No orphaned pages (warn only)
    - Blog posts have required frontmatter (checked during parsing)
    - No circular references (not possible with current structure)

    Args:
        site: Site object to validate

    Returns:
        List of warning/error messages. Empty if all valid.
    """
    warnings = []

    # Check for orphaned pages
    if site.orphaned_pages:
        warnings.append(
            f"Found {len(site.orphaned_pages)} orphaned pages (not in any category)"
        )

    # Check each category has pages (warn if empty)
    for cat_name, category in site.categories.items():
        if not category.pages:
            warnings.append(f"Category '{cat_name}' has no pages (only root page)")

    return warnings
