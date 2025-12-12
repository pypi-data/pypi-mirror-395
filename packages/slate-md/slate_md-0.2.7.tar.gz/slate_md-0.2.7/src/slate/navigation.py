"""Navigation generation for Slate sites.

This module generates navigation HTML for multi-page sites,
including header navigation and category-specific navigation.
"""

from typing import Any

from slate.site import Category, Site


class NavigationGenerator:
    """Generates navigation HTML for templates."""

    @staticmethod
    def generate_header_nav(site: Site, current_page: Any = None) -> str:
        """Generate header navigation linking to all category root pages.

        This creates a simple list of links to each category root page.
        Templates can style this however they want.

        Args:
            site: The Site object with categories
            current_page: The current Page object (optional) for relative path calculation

        Returns:
            HTML string with navigation links

        Example output:
            <a href="blog.html">Blog</a>
            <a href="projects.html">Projects</a>
        """
        import os

        links = []
        for _cat_name, category in sorted(site.categories.items()):
            label = category.root_page.title

            # Calculate relative path if current_page is provided
            if current_page:
                # Get relative path from current page's directory to the category root page
                # We need to go from current_page.output_path.parent to category.root_page.output_path
                try:
                    rel_path = os.path.relpath(
                        category.root_page.output_path, current_page.output_path.parent
                    )
                    href = rel_path
                except ValueError:
                    # Fallback if paths are on different drives or something weird
                    href = category.root_page.output_path.name
            else:
                # Fallback to simple filename (works for flat structure or root)
                href = category.root_page.output_path.name

            links.append(f'<a href="{href}" class="content-nav_header">{label}</a>')

        return "\n".join(links)

    @staticmethod
    def generate_category_nav(category: Category, current_page: Any = None) -> str:
        """Generate category-specific navigation for pages within a category.

        Creates an unordered list of links to all pages in the category.
        For blog categories, shows blog posts in date order (newest first).

        Args:
            category: The Category object
            current_page: The current Page object (optional) for relative path calculation

        Returns:
            HTML string with navigation list
        """
        if not category.pages:
            return ""

        # Use blog posts if category has them (sorted by date)
        pages_to_show = category.blog_posts if category.blog_posts else category.pages

        links = []
        import os

        for page in pages_to_show:
            title = page.title

            # Calculate href
            if current_page:
                try:
                    # Calculate relative path from current page's directory to target page
                    rel_path = os.path.relpath(
                        page.output_path, current_page.output_path.parent
                    )
                    href = rel_path
                except ValueError:
                    href = page.output_path.name
            else:
                href = page.output_path.name

            # For blog posts, optionally include date
            if page.is_blog_post and "date" in page.frontmatter:
                date = page.frontmatter["date"]
                # Format date (handle both datetime.date and string)
                date_str = str(date) if hasattr(date, "__str__") else date
                links.append(
                    f'  <li><a href="{href}" class="content-nav_category">{title}</a> <span class="date">({date_str})</span></li>'
                )
            else:
                links.append(
                    f'  <li><a href="{href}" class="content-nav_category">{title}</a></li>'
                )

        return "<ul>\n" + "\n".join(links) + "\n</ul>"

    @staticmethod
    def generate_breadcrumbs(
        page_category: str | None, site: Site, current_page: Any = None
    ) -> str:
        """Generate breadcrumb navigation.

        Args:
            page_category: Category of current page (None for index)
            site: The Site object
            current_page: The current Page object (optional)

        Returns:
            HTML breadcrumb string
        """
        # If no category and no current page (or current page is index), return empty
        if not page_category and (not current_page or current_page == site.index_page):
            return ""

        import os

        # Helper to get relative path to root or other pages
        def get_rel_href(target_path):
            if current_page:
                try:
                    return os.path.relpath(target_path, current_page.output_path.parent)
                except ValueError:
                    return target_path.name
            return target_path.name

        # Start with Home
        # Home is site.index_page
        home_href = get_rel_href(site.index_page.output_path)
        crumbs = [(f'<a href="{home_href}" class="breadcrumb">Home</a>', home_href)]

        # Add Category if present
        if page_category and page_category in site.categories:
            cat = site.categories[page_category]
            cat_href = get_rel_href(cat.root_page.output_path)
            crumbs.append(
                (
                    f'<a href="{cat_href}" class="breadcrumb">{cat.root_page.title}</a>',
                    cat_href,
                )
            )

        # Add Current Page if it's not the category root
        if current_page:
            is_cat_root = False
            if (
                page_category
                and page_category in site.categories
                and site.categories[page_category].root_page == current_page
            ):
                is_cat_root = True

            if not is_cat_root and current_page != site.index_page:
                # Link to self (relative is just filename)
                self_href = current_page.output_path.name
                crumbs.append(
                    (
                        f'<a href="{self_href}" class="breadcrumb current">{current_page.title}</a>',
                        self_href,
                    )
                )

        # Join with separator
        separator = ' <span class="breadcrumb-separator">/</span> '
        html = separator.join(c[0] for c in crumbs)

        return f'<nav class="breadcrumbs">{html}</nav>'


def build_navigation_context(
    site: Site, current_category: str | None = None, current_page: Any = None
) -> dict[str, Any]:
    """Build navigation context dictionary for template rendering.

    This creates a context dict with all navigation-related variables
    that can be injected into templates.

    Args:
        site: The Site object
        current_category: Category of the current page (None for index)
        current_page: The current Page object (optional)

    Returns:
        Dictionary with navigation variables:
        - nav_header: Header navigation HTML
        - nav_category: Category navigation HTML (if in a category)
        - category_name: Name of current category (if in a category)
        - breadcrumbs: Breadcrumb navigation HTML
    """
    nav_gen = NavigationGenerator()

    context = {
        "nav_header": nav_gen.generate_header_nav(site, current_page),
        "nav_category": "",
        "category_name": current_category or "",
        "breadcrumbs": nav_gen.generate_breadcrumbs(
            current_category, site, current_page
        ),
    }

    # Add category-specific navigation if in a category
    if current_category and current_category in site.categories:
        category = site.categories[current_category]
        context["nav_category"] = nav_gen.generate_category_nav(category, current_page)

    return context
