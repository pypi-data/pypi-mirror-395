"""RSS feed generation for Slate blog posts.

This module generates RSS 2.0 feeds for categories containing blog posts.
"""

from datetime import date, datetime
from typing import Any
from xml.etree import ElementTree as ET  # nosec B405

from slate.site import Category


def generate_rss_feed(
    category: Category, site_url: str, site_title: str, site_description: str = ""
) -> str:
    """Generate RSS 2.0 feed for blog posts in a category.

    Only includes pages with type: blog.
    Sorts by date (newest first).

    Args:
        category: Category containing blog posts
        site_url: Base URL of the site (e.g., "https://example.com")
        site_title: Title of the site
        site_description: Description of the site/category

    Returns:
        RSS 2.0 XML string

    Example:
        >>> feed = generate_rss_feed(category, "https://blog.example.com", "My Blog")
        >>> print(feed)
        <?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">...</rss>
    """
    # Create RSS root element
    rss = ET.Element(
        "rss", version="2.0", attrib={"xmlns:atom": "http://www.w3.org/2005/Atom"}
    )
    channel = ET.SubElement(rss, "channel")

    # Channel metadata
    ET.SubElement(channel, "title").text = f"{site_title} - {category.name.title()}"

    # Build category URL
    category_url = f"{site_url.rstrip('/')}/{category.root_page.output_path.name}"
    ET.SubElement(channel, "link").text = category_url

    # Description
    desc = site_description or f"{category.name.title()} posts from {site_title}"
    ET.SubElement(channel, "description").text = desc

    # Add atom:link for feed self-reference
    feed_url = f"{site_url.rstrip('/')}/{category.name}/feed.xml"
    ET.SubElement(
        channel,
        "{http://www.w3.org/2005/Atom}link",
        attrib={"href": feed_url, "rel": "self", "type": "application/rss+xml"},
    )

    # Get blog posts (already sorted by date, newest first)
    blog_posts = category.blog_posts

    if not blog_posts:
        # No blog posts, return minimal feed
        return _format_xml(rss)

    # Add items for each blog post
    for post in blog_posts:
        item = ET.SubElement(channel, "item")

        # Title
        ET.SubElement(item, "title").text = post.title

        # Link - build full URL
        post_url = f"{site_url.rstrip('/')}/{post.output_path}"
        ET.SubElement(item, "link").text = str(post_url)

        # Description
        description = post.frontmatter.get("description", "")
        if description:
            ET.SubElement(item, "description").text = description

        # Publication date in RFC 822 format
        post_date = post.frontmatter.get("date")
        if post_date:
            pub_date = _format_rfc822_date(post_date)
            ET.SubElement(item, "pubDate").text = pub_date

        # Author (optional)
        author = post.frontmatter.get("author")
        if author:
            ET.SubElement(item, "author").text = author

        # GUID (unique identifier)
        ET.SubElement(item, "guid", isPermaLink="true").text = str(post_url)

    return _format_xml(rss)


def _format_rfc822_date(date_value: Any) -> str:
    """Format a date value to RFC 822 format required by RSS.

    Args:
        date_value: Either a datetime.date object or ISO date string

    Returns:
        RFC 822 formatted date string (e.g., "Mon, 01 Dec 2024 00:00:00 +0000")
    """
    if isinstance(date_value, str):
        # Parse ISO date string
        date_obj = datetime.fromisoformat(date_value).date()
    elif isinstance(date_value, datetime):
        date_obj = date_value.date()
    elif isinstance(date_value, date):
        date_obj = date_value
    else:
        # Fallback to current date
        date_obj = datetime.now().date()

    # Convert to datetime at midnight UTC
    dt = datetime.combine(date_obj, datetime.min.time())

    # Format as RFC 822
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")


def _format_xml(root: ET.Element) -> str:
    """Format XML element tree with proper indentation and declaration.

    Args:
        root: Root XML element

    Returns:
        Formatted XML string with declaration
    """
    # Add indentation for readability
    _indent(root)

    # Convert to string
    xml_str = ET.tostring(root, encoding="unicode", method="xml")

    # Add XML declaration
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_str


def _indent(elem: ET.Element, level: int = 0) -> None:
    """Add indentation to XML elements for pretty printing.

    Args:
        elem: XML element to indent
        level: Current indentation level
    """
    indent_str = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent_str + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent_str
        for child in elem:
            _indent(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = indent_str
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent_str
