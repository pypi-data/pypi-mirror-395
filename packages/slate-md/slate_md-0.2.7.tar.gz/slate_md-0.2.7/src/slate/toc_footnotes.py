"""
Enhanced parse.py with TOC and footnotes support.

This adds table of contents generation and footnotes parsing to the existing
parse module.
"""

# Add these functions at the end of parse.py

import re
from typing import Any


def generate_toc(blocks: list[dict[str, Any]]) -> str:
    """Generate table of contents HTML from heading blocks.
    
    Extracts all h1-h6 headings and creates a nested HTML list with slugified
    anchor links.
    
    Args:
        blocks: List of parsed Markdown blocks
        
    Returns:
        HTML string with table of contents, or empty string if no headings
        
    Example:
        >>> blocks = [{"h1": "Introduction"}, {"h2": "Overview"}]
        >>> toc = generate_toc(blocks)
        >>> print(toc)
        <nav class="toc">
          <ul>
            <li><a href="#introduction">Introduction</a></li>
            <li class="toc-h2"><a href="#overview">Overview</a></li>
          </ul>
        </nav>
    """
    toc_items = []
    
    # Extract heading information
    for block in blocks:
        for level_key in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            if level_key in block:
                text = block[level_key]
                level = int(level_key[1])
                slug = slugify(text)
                toc_items.append({
                    "level": level,
                    "text": text,
                    "slug": slug
                })
                break  # Only one heading per block
    
    if not toc_items:
        return ""
    
    # Build HTML
    html_lines = ['<nav class="toc">', '  <ul>']
    
    for item in toc_items:
        level_class = f' class="toc-h{item["level"]}"' if item["level"] > 1 else ""
        html_lines.append(
            f'    <li{level_class}><a href="#{item["slug"]}">{item["text"]}</a></li>'
        )
    
    html_lines.extend(['  </ul>', '</nav>'])
    
    return '\n'.join(html_lines)


def slugify(text: str) -> str:
    """Convert text to URL-safe slug.
    
    Args:
        text: Text to slugify
        
    Returns:
        Lowercase, hyphenated slug
        
    Example:
        >>> slugify("Hello World!")
        'hello-world'
        >>> slugify("C++ Programming")
        'c-programming'
    """
    # Lowercase
    slug = text.lower()
    
    # Remove non-word characters (except spaces and hyphens)
    slug = re.sub(r'[^\w\s-]', '', slug)
    
    # Replace spaces and multiple hyphens with single hyphen
    slug = re.sub(r'[-\s]+', '-', slug)
    
    # Strip leading/trailing hyphens
    return slug.strip('-')


def parse_footnotes(md_text: str) -> tuple[str, dict[str, str]]:
    """Parse footnotes from Markdown text.
    
    Footnotes use syntax:
        Here's text with footnote[^1].
        
        [^1]: This is the footnote.
    
    Args:
        md_text: Markdown text with potential footnotes
        
    Returns:
        Tuple of (text_without_footnote_defs, footnotes_dict)
        where footnotes_dict maps footnote IDs to their text
        
    Example:
        >>> text = "Hello[^1]\\n\\n[^1]: World"
        >>> content, footnotes = parse_footnotes(text)
        >>> print(content)
        Hello[^1]
        >>> print(footnotes)
        {'1': 'World'}
    """
    # Pattern to match footnote definitions
    footnote_pattern = r'^\[\^(\w+)\]:\s*(.+)$'
    footnotes = {}
    lines = []
    
    for line in md_text.split('\n'):
        match = re.match(footnote_pattern, line)
        if match:
            footnotes[match.group(1)] = match.group(2).strip()
        else:
            lines.append(line)
    
    return '\n'.join(lines), footnotes


def render_footnotes(footnotes: dict[str, str]) -> str:
    """Render footnotes as HTML.
    
    Args:
        footnotes: Dictionary mapping footnote IDs to their text
        
    Returns:
        HTML div with footnotes list, or empty string if no footnotes
        
    Example:
        >>> footnotes = {'1': 'First note', '2': 'Second note'}
        >>> html = render_footnotes(footnotes)
        >>> '<div class="footnotes">' in html
        True
    """
    if not footnotes:
        return ""
    
    html_lines = ['<div class="footnotes">', '  <hr>', '  <ol>']
    
    for key, text in sorted(footnotes.items()):
        html_lines.append(
            f'    <li id="fn-{key}">{text} <a href="#fnref-{key}" class="footnote-backref">↩</a></li>'
        )
    
    html_lines.extend(['  </ol>', '</div>'])
    
    return '\n'.join(html_lines)


def replace_footnote_refs(html: str) -> str:
    """Replace footnote reference markers with HTML links.
    
    Converts [^1] to <sup><a href="#fn-1" id="fnref-1">[1]</a></sup>
    
    Args:
        html: HTML content with [^n] markers
        
    Returns:
        HTML with footnote references as superscript links
    """
    def replace_fn_ref(match):
        footnote_id = match.group(1)
        return f'<sup><a href="#fn-{footnote_id}" id="fnref-{footnote_id}" class="footnote-ref">[{footnote_id}]</a></sup>'
    
    return re.sub(r'\[\^(\w+)\]', replace_fn_ref, html)
