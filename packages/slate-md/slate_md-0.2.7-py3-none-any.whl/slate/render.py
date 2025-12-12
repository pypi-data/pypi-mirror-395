"""Render block-oriented Markdown ASTs into several output formats.

This module provides three renderer classes:

- ``HTMLRenderer``: converts block dicts to HTML strings.
- ``GemtextRenderer``: produces gemtext (Gemini) text output.
- ``GopherRenderer``: emits a simple gophermap-like text representation.

Helpers and lightweight backward-compatible wrappers are provided at the
module level (`render_block`, `render_blocks`) so existing imports continue
to work.
"""

import html
import re
from collections.abc import Callable
from typing import Any

from slate.parse import render_footnotes, replace_footnote_refs

# Constants for supported HTML tags and callout types
HEADINGS = ("h1", "h2", "h3", "h4", "h5", "h6")
CALLOUTS = (
    "note",
    "warning",
    "danger",
    "success",
    "tip",
)


# Precompile commonly-used regexes to avoid repeated compilation at runtime.
# Regex for matching Markdown image syntax: ![alt text](src "caption")
IMAGE_RE = re.compile(
    r'!\[(?P<alt>[^\]]*)\]\((?P<src>[^\s\)]+)(?:\s+"(?P<caption>[^\"]*)")?\)'
)
# Regex for matching Markdown link syntax: [label](href)
LINK_RE = re.compile(r"\[(?P<label>[^\]]+)\]\((?P<href>[^\)]+)\)")
# Regex for matching generic custom token syntax: [!TOKEN] [label](href)
CUSTOM_TOKEN_RE = re.compile(
    r"\[!(?P<token>[A-Z0-9-_]+)\]\s*\[(?P<label>[^\]]+)\]\((?P<href>[^\)]+)\)"
)
# Regex for matching inline code: `code`
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
# Regex for matching bold text: **text** or __text__
BOLD_RE = re.compile(r"(\*\*|__)(?P<content>.+?)\1")
# Regex for matching italic text: *text* or _text_
ITALIC_RE = re.compile(r"(\*|_)(?P<content>.+?)\1")
# Regex for matching strikethrough text: ~~text~~
STRIKE_RE = re.compile(r"~~(?P<content>.+?)~~")
# Regex for matching tip token: [!TIP]
TIP_RE = re.compile(r"\[!TIP\]")


def _escape(value: Any) -> str:
    """Return an HTML-escaped string for the given value.

    The renderer escapes values before inserting them into HTML output. Other
    formats (gemtext/gopher) intentionally emit raw text and therefore do not
    use HTML escaping.
    """

    return html.escape("" if value is None else str(value), quote=True)


def _img_replace(match: re.Match) -> str:
    """Replaces a Markdown image pattern with its corresponding HTML <figure> tag.

    This helper function is used by `render_inline_links` to convert image
    Markdown into HTML, handling alt text, source, and optional captions.

    Args:
        match: A regex match object containing groups for 'alt', 'src', and 'caption'.

    Returns:
        An HTML string representing the image within a <figure> and <figcaption> if a caption is present.
    """
    # Extract alt text, source, and caption from the regex match.
    # Escape HTML sensitive characters to prevent cross-site scripting (XSS).
    alt_text = _escape(match.group("alt"))
    image_source = _escape(match.group("src"))
    caption_raw = match.group("caption") or ""
    image_caption = _escape(
        caption_raw.strip(' "')
    )  # Strip quotes and extra spaces from caption.

    # Construct the base HTML for the image figure.
    figure_html = f'<figure class="content-figure"><img src="{image_source}" alt="{alt_text}" class="content-image"/>'
    # If a caption exists, add a <figcaption> tag.
    if image_caption:
        figure_html += (
            f'<figcaption class="content-figcaption">{image_caption}</figcaption>'
        )
    figure_html += "</figure>"
    return figure_html


def _link_replace(match: re.Match) -> str:
    """Replaces a Markdown link pattern with its corresponding HTML <a> tag.

    This helper function is used by `render_inline_links` to convert link
    Markdown into HTML.

    Args:
        match: A regex match object containing groups for 'label' and 'href'.

    Returns:
        An HTML string representing the hyperlink.
    """
    # Extract label and href from the regex match.
    # Escape HTML sensitive characters.
    link_label = _escape(match.group("label"))
    link_href = _escape(match.group("href"))
    # Construct the HTML anchor tag.
    return f'<a href="{link_href}" class="content-link">{link_label}</a>'


class CustomTokenRegistry:
    """Registry for custom Markdown tokens."""

    _handlers: dict[str, Callable[[re.Match], str]] = {}

    @classmethod
    def register(cls, token_name: str, handler: Callable[[re.Match], str]) -> None:
        """Register a handler for a specific token name."""
        cls._handlers[token_name.upper()] = handler

    @classmethod
    def get_handler(cls, token_name: str) -> Callable[[re.Match], str] | None:
        """Get the handler for a specific token name."""
        return cls._handlers.get(token_name.upper())


def _md_page_link_handler(match: re.Match) -> str:
    """Handler for MD-PAGE token.

    Replaces a special MD-PAGE link pattern with its corresponding HTML <a> tag, converting extension.
    """
    link_label = _escape(match.group("label"))
    link_href = match.group("href")

    # Convert .md extension to .html
    if link_href.lower().endswith(".md"):
        link_href = link_href[:-3] + ".html"

    link_href = _escape(link_href)
    return f'<a href="{link_href}" class="content-md_page">{link_label}</a>'


# Register the default MD-PAGE handler
CustomTokenRegistry.register("MD-PAGE", _md_page_link_handler)


def _button_handler(match: re.Match) -> str:
    """Handler for BUTTON token.

    Replaces [!BUTTON] [Label](Link) with <button class="content-button" onclick="window.location.href='Link'">Label</button>
    """
    label = _escape(match.group("label"))
    href = _escape(match.group("href"))
    return f'<button class="content-button" onclick="window.location.href=\'{href}\'">{label}</button>'


CustomTokenRegistry.register("BUTTON", _button_handler)


def _external_link_handler(match: re.Match) -> str:
    """Handler for EXTERNAL token.

    Replaces [!EXTERNAL] [Label](Link) with <a href="Link" class="content-external">Label</a>
    Auto-detects protocol if missing and simplifies label if it's a URL.
    """
    label = _escape(match.group("label"))
    href = _escape(match.group("href"))

    # Auto-prepend protocol for specific types that are often mistaken for relative paths
    if not re.match(r"^[a-zA-Z0-9]+://", href) and not href.startswith(
        ("/", "./", "../")
    ):
        if href.endswith(".onion"):
            href = f"http://{href}"
        elif href.endswith(".gopher"):
            href = f"gopher://{href}"
        elif href.endswith(".gemini"):
            href = f"gemini://{href}"
        elif href.endswith(".eth") or href.startswith("www."):
            href = f"https://{href}"

    # Simplify label: remove protocol and www for display
    clean_label = re.sub(r"^[a-zA-Z0-9]+://", "", label)
    clean_label = re.sub(r"^www\.", "", clean_label)

    return f'<a href="{href}" class="content-external">{clean_label}</a>'


CustomTokenRegistry.register("EXTERNAL", _external_link_handler)


def _custom_token_replace(match: re.Match) -> str:
    """Dispatcher for custom tokens."""
    token = match.group("token")
    handler = CustomTokenRegistry.get_handler(token)
    if handler:
        return handler(match)
    return match.group(0)


def replace_tipping_token(text: str, renderer: Any) -> str:
    """Replaces the [!TIP] token with appropriate content based on renderer type."""

    def _handler(match: re.Match) -> str:
        if not renderer or not renderer.page or not renderer.page.frontmatter:
            return ""
        tipping = renderer.page.frontmatter.get("tipping", {})
        if not tipping:
            return ""

        is_gemini = renderer.__class__.__name__ == "GemtextRenderer"

        lines = []
        if is_gemini:
            lines.append("Support:")
            for network, address in tipping.items():
                label = network.upper()
                if network == "kofi":
                    lines.append(f"=> https://ko-fi.com/{address} Ko-fi")
                else:
                    lines.append(f"* {label}: {address}")
        else:
            # Gopher or plain text
            lines.append("Support:")
            for network, address in tipping.items():
                label = network.upper()
                if network == "kofi":
                    lines.append(f"Ko-fi: https://ko-fi.com/{address}")
                else:
                    lines.append(f"- {label}: {address}")

        return "\n".join(lines)

    return TIP_RE.sub(_handler, text)


def resolve_link(
    href: str,
    site: Any = None,
    current_page: Any = None,
    ipfs: bool = False,
    renderer: Any = None,
) -> str:
    """Resolves a link to a relative path if possible, handling .md to .html/.gmi conversion.

    Args:
        href: The link target.
        site: Site object.
        current_page: Current Page object.
        ipfs: Whether to force relative paths (IPFS mode).
        renderer: Renderer instance for format-specific handling.

    Returns:
        Resolved link.
    """
    if not (site and current_page):
        return href

    # If it's an external link, return as is
    if href.startswith(("http://", "https://", "mailto:", "gopher://", "gemini://")):
        return href

    # If it's an anchor, return as is
    if href.startswith("#"):
        return href

    # If it's a markdown file, try to resolve it
    if href.endswith(".md"):
        try:
            target_source = None
            if href.startswith("/"):
                # Absolute path from site root
                target_source = (site.root_path / href.lstrip("/")).resolve()
            else:
                # Relative path
                target_source = (current_page.source_path.parent / href).resolve()

            # Find page with this source path
            target_page = None

            # Check index
            if site.index_page.source_path.resolve() == target_source:
                target_page = site.index_page

            # Check categories
            if not target_page:
                for category in site.categories.values():
                    if category.root_page.source_path.resolve() == target_source:
                        target_page = category.root_page
                        break
                    for page in category.pages:
                        if page.source_path.resolve() == target_source:
                            target_page = page
                            break
                    if target_page:
                        break

            if target_page:
                # Calculate relative path from current output to target output
                import os

                rel_path = os.path.relpath(
                    target_page.output_path, current_page.output_path.parent
                )

                # Swap extension based on renderer
                if (
                    renderer
                    and renderer.__class__.__name__ == "GemtextRenderer"
                    and rel_path.endswith(".html")
                ):
                    rel_path = rel_path[:-5] + ".gmi"

                return rel_path
            else:
                # Fallback: just replace extension
                ext = ".html"
                if renderer and renderer.__class__.__name__ == "GemtextRenderer":
                    ext = ".gmi"
                return href[:-3] + ext
        except Exception:
            # If resolution fails, fallback to simple replacement
            return href[:-3] + ".html"

    # If IPFS is on, and it's NOT a .md file (e.g. .html, .css, .png), we still need to fix absolute paths.
    if ipfs and href.startswith("/") and not href.startswith("//"):
        try:
            if site and site.index_page:
                root_dir = site.index_page.output_path.parent
                current_dir = current_page.output_path.parent

                # Calculate relative path from current to root
                import os

                rel_to_root = os.path.relpath(root_dir, current_dir)

                # Now append the href (without leading slash)
                target = os.path.join(rel_to_root, href.lstrip("/"))
                return target
        except Exception:
            pass

    return href


def render_inline_links(
    text: str,
    site: Any = None,
    current_page: Any = None,
    ipfs: bool = False,
    renderer: Any = None,
) -> str:
    """Replaces inline Markdown images, links, code, and formatting with their HTML equivalents.

    Args:
        text: The input text string.
        site: Optional Site object for resolving links.
        current_page: Optional Page object for relative path calculation.
        ipfs: If True, forces all internal links to be relative.
        renderer: Optional Renderer instance for context-aware rendering (tipping, format).

    Returns:
        The text string with Markdown inline elements replaced by HTML.
    """

    # Use renderer context if available
    if renderer:
        site = getattr(renderer, "site", site)
        current_page = getattr(renderer, "page", current_page)
        ipfs = getattr(renderer, "ipfs", ipfs)

    # 1. Protect Code Blocks
    # We replace inline code with placeholders to prevent formatting/links from affecting code content.
    placeholders: list[str] = []

    def code_replacer(match: re.Match) -> str:
        # Escape the code content immediately
        code_html = f'<code class="content-code">{html.escape(match.group(1))}</code>'
        placeholders.append(code_html)
        # Use a placeholder that doesn't trigger Bold (__) or Italic (_) regexes
        return f"%%SLATECODEBLOCK{len(placeholders) - 1}%%"

    text = INLINE_CODE_RE.sub(code_replacer, text)

    # 2. Replace Images
    text = IMAGE_RE.sub(_img_replace, text)

    # 3. Replace Custom Tokens (generic)
    text = CUSTOM_TOKEN_RE.sub(_custom_token_replace, text)

    # 4. Replace Tipping Token
    def _tip_handler(match: re.Match) -> str:
        if not renderer or not renderer.page or not renderer.page.frontmatter:
            return ""

        tipping = renderer.page.frontmatter.get("tipping", {})
        if not tipping:
            return ""

        # Determine output format based on renderer type
        is_html = renderer.__class__.__name__ == "HTMLRenderer"
        is_gemini = renderer.__class__.__name__ == "GemtextRenderer"
        is_gopher = renderer.__class__.__name__ == "GopherRenderer"

        if is_html:
            options = []
            for network, address in tipping.items():
                label = network.upper()
                if network == "kofi":
                    options.append(
                        f'<a href="https://ko-fi.com/{address}" class="content-link">Ko-fi</a>'
                    )
                else:
                    options.append(
                        f'<span class="content-tip-option"><strong>{label}:</strong> {address}</span>'
                    )
            return f'<div class="content-tip"><strong>Support:</strong> {" | ".join(options)}</div>'

        elif is_gemini:
            lines = ["Support:"]
            for network, address in tipping.items():
                label = network.upper()
                if network == "kofi":
                    lines.append(f"=> https://ko-fi.com/{address} Ko-fi")
                else:
                    lines.append(f"* {label}: {address}")
            return "\n".join(lines)

        elif is_gopher:
            lines = ["Support:"]
            for network, address in tipping.items():
                label = network.upper()
                if network == "kofi":
                    lines.append(
                        f"hKo-fi\tURL:https://ko-fi.com/{address}\tlocalhost\t70"
                    )
                else:
                    lines.append(f"i- {label}: {address}\t\tlocalhost\t70")
            return "Support: " + ", ".join(
                f"{k.upper()}: {v}" for k, v in tipping.items()
            )

        return ""

    text = TIP_RE.sub(_tip_handler, text)

    # 4. Custom token replacer that handles MD-PAGE specifically with context
    def custom_token_replacer_with_context(match: re.Match) -> str:
        token = match.group("token")
        if token == "MD-PAGE":  # nosec B105
            # Handle MD-PAGE with smart resolution
            label = _escape(match.group("label"))
            href = match.group("href")

            # Apply smart resolution
            resolved_href = resolve_link(href, site, current_page, ipfs, renderer)

            # Ensure extension is .html if it was .md
            if resolved_href.lower().endswith(".md"):
                resolved_href = resolved_href[:-3] + ".html"

            return f'<a href="{_escape(resolved_href)}" class="content-md_page">{label}</a>'
        else:
            # Delegate to registry for other tokens
            return _custom_token_replace(match)

    # Replace custom tokens using the context-aware replacer
    text = CUSTOM_TOKEN_RE.sub(custom_token_replacer_with_context, text)

    # 5. Replace Links
    def link_replacer(match: re.Match) -> str:
        label = _escape(match.group("label"))
        href = match.group("href")

        # If it's an external link or anchor, leave it alone
        if href.startswith(
            ("http://", "https://", "#", "mailto:", "gopher://", "gemini://")
        ):
            return f'<a href="{_escape(href)}" class="content-link">{label}</a>'

        # Apply smart resolution (handles .md and IPFS relative paths)
        href = resolve_link(href, site, current_page, ipfs, renderer)

        # Simple extension replacement for .md files (if not handled by smart link)
        if href.lower().endswith(".md"):
            href = href[:-3] + ".html"

        return f'<a href="{_escape(href)}" class="content-link">{label}</a>'

    text = LINK_RE.sub(link_replacer, text)

    # 6. Apply Formatting (Bold, Italic, Strike)
    # Order matters: Bold before Italic
    text = BOLD_RE.sub(r'<strong class="content-strong">\g<content></strong>', text)
    text = ITALIC_RE.sub(r'<em class="content-em">\g<content></em>', text)
    text = STRIKE_RE.sub(r'<del class="content-del">\g<content></del>', text)

    # 7. Restore Code Blocks
    for i, code_html in enumerate(placeholders):
        text = text.replace(f"%%SLATECODEBLOCK{i}%%", code_html)

    return text


def render_inline_text(text: str, renderer: Any = None) -> str:
    """Renders text for text-only formats (Gemtext/Gopher), stripping HTML/Markdown formatting.

    Args:
        text: The input text with Markdown formatting.

    Returns:
        Clean text with formatting stripped.
    """
    if not text:
        return ""

    # Strip Bold
    text = BOLD_RE.sub(r"\g<content>", text)
    # Strip Italic
    text = ITALIC_RE.sub(r"\g<content>", text)
    # Strip Strike
    text = STRIKE_RE.sub(r"\g<content>", text)
    # Strip Code
    text = INLINE_CODE_RE.sub(r"\1", text)

    # Replace Links [label](url) -> label
    text = LINK_RE.sub(r"\g<label>", text)

    # Replace Images ![alt](src) -> [Image: alt]
    text = IMAGE_RE.sub(r"[Image: \g<alt>]", text)

    # Custom Tokens
    # MD-PAGE -> label
    text = re.sub(
        r"\[!MD-PAGE\]\s*\[(?P<label>[^\]]+)\]\((?P<href>[^\)]+)\)",
        r"\g<label>",
        text,
    )

    # Tipping Token
    text = replace_tipping_token(text, renderer)

    # Generic Custom Token -> label
    # BUTTON -> [Button: label]
    text = re.sub(
        r"\[!BUTTON\]\s*\[(?P<label>[^\]]+)\]\((?P<href>[^\)]+)\)",
        r"[Button: \g<label>]",
        text,
    )
    # EXTERNAL -> label
    text = re.sub(
        r"\[!EXTERNAL\]\s*\[(?P<label>[^\]]+)\]\((?P<href>[^\)]+)\)", r"\g<label>", text
    )

    return text


class VariableRegistry:
    """Registry for template variables."""

    _handlers: dict[str, Callable[[dict[str, Any]], str]] = {}

    @classmethod
    def register(cls, name: str, handler: Callable[[dict[str, Any]], str]):
        """Register a handler for a variable name."""
        cls._handlers[name] = handler

    @classmethod
    def get_value(cls, name: str, context: dict[str, Any]) -> str:
        """Get the value of a variable given the context."""
        handler = cls._handlers.get(name)
        if handler:
            return handler(context)
        return ""


# Register default variables
VariableRegistry.register("creation_date", lambda c: c.get("creation_date", ""))
VariableRegistry.register("creation_time", lambda c: c.get("creation_time", ""))
VariableRegistry.register("modify_date", lambda c: c.get("modify_date", ""))
VariableRegistry.register("modify_time", lambda c: c.get("modify_time", ""))
VariableRegistry.register("version", lambda c: c.get("version", ""))
VariableRegistry.register(
    "datetime",
    lambda c: " ".join(
        x for x in (c.get("creation_date", ""), c.get("creation_time", "")) if x
    ),
)

# Navigation variables (v0.2.0)
VariableRegistry.register("nav_header", lambda c: c.get("nav_header", ""))
VariableRegistry.register("nav_category", lambda c: c.get("nav_category", ""))
VariableRegistry.register("category_name", lambda c: c.get("category_name", ""))
VariableRegistry.register("breadcrumbs", lambda c: c.get("breadcrumbs", ""))

# Content enhancement variables (v0.2.0)
VariableRegistry.register("toc", lambda c: c.get("toc", ""))


class BaseRenderer:
    """Base class for all renderers."""

    def __init__(self):
        self.title: str | None = None
        self.description: str | None = None
        self.creation_date: str | None = None
        self.creation_time: str | None = None
        self.modify_date: str | None = None
        self.modify_time: str | None = None
        self.version: str | None = None
        self.site: Any = None
        self.page: Any = None
        self.toc: str | None = None
        self.footnotes: dict[str, str] = {}

    def _apply_dt(self, s: str | None) -> str:
        """Applies variable placeholders to a string using the VariableRegistry."""
        if s is None:
            return ""

        context = {
            "title": self.title,
            "description": self.description,
            "creation_date": self.creation_date,
            "creation_time": self.creation_time,
            "modify_date": self.modify_date,
            "modify_time": self.modify_time,
            "version": self.version,
            "toc": self.toc,
        }
        # We need to find all {{variable}} patterns and replace them
        # A simple regex for {{name}}
        return re.sub(
            r"\{\{([a-zA-Z0-9-_]+)\}\}",
            lambda m: VariableRegistry.get_value(m.group(1), context),
            s,
        )

    def render_blocks(
        self,
        blocks: list[dict[str, Any]],
        title: str | None = None,
        description: str | None = None,
        creation_date: str | None = None,
        creation_time: str | None = None,
        modify_date: str | None = None,
        modify_time: str | None = None,
        version: str | None = None,
        site: Any = None,
        page: Any = None,
        toc: str | None = None,
        footnotes: dict[str, str] | None = None,
        ipfs: bool = False,
        host: str = "localhost",
        port: int = 70,
        **kwargs,
    ) -> str:
        """Renders a list of blocks. Subclasses must implement specific logic."""
        self.title = title
        self.description = description
        self.creation_date = creation_date
        self.creation_time = creation_time
        self.modify_date = modify_date
        self.modify_time = modify_time
        self.version = version
        self.site = site
        self.page = page
        self.toc = toc
        self.footnotes = footnotes or {}
        self.ipfs = ipfs
        return ""


class HTMLRenderer(BaseRenderer):
    """Renders a list of Markdown block dictionaries into an HTML string.

    This renderer converts the structured block data generated by the parser
    into standard HTML tags, applying appropriate styling classes and handling
    various Markdown elements suchs as headings, paragraphs, lists, code blocks,
    images, blockquotes, callouts, and tables. It also supports dynamic
    replacement of `{{date}}` and `{{time}}` placeholders within the content.
    """

    def render_block(self, block: dict[str, Any]) -> str:
        """Renders a single Markdown block dictionary into its HTML string representation."""

        # Render Headings (h1, h2, etc.)
        for tag_name in HEADINGS:
            if tag_name in block:
                # Construct HTML class for styling (e.g., 'content-h1').
                css_classes = f"content-{tag_name}"
                # Escape content and replace date/time placeholders.
                content = _escape(self._apply_dt(block[tag_name]))
                return f"<{tag_name} class='{css_classes}'>{content}</{tag_name}>"

        # Render Paragraphs
        if "p" in block:
            # Escape content, replace date/time placeholders, and handle inline links/images.
            processed_content = render_inline_links(
                self._apply_dt(block["p"]),
                site=self.site,
                current_page=self.page,
                ipfs=getattr(self, "ipfs", False),
                renderer=self,
            )
            return f"<p class='content-paragraph'>{processed_content}</p>"

        # Render Blockquotes
        if "blockquote" in block:
            content = block["blockquote"]
            if isinstance(content, list):
                # Recursive rendering for nested blocks
                inner_html = self.render_blocks(
                    content,
                    site=self.site,
                    page=self.page,
                    ipfs=getattr(self, "ipfs", False),
                )
                return (
                    f"<blockquote class='content-blockquote'>{inner_html}</blockquote>"
                )
            else:
                # Legacy string rendering
                blockquote_content = _escape(self._apply_dt(content))
                return f"<blockquote class='content-blockquote'><p>{blockquote_content}</p></blockquote>"

        # Render Callouts (e.g., [!NOTE], [!WARNING])
        for callout_type in CALLOUTS:
            block_key = f"callout-{callout_type}"
            if block_key in block:
                # Capitalize the callout type for display (e.g., "Note", "Warning").
                display_title = callout_type.capitalize()
                content = block[block_key]

                if isinstance(content, list):
                    # Recursive rendering for nested blocks
                    inner_html = self.render_blocks(
                        content,
                        site=self.site,
                        page=self.page,
                        ipfs=getattr(self, "ipfs", False),
                    )
                    return (
                        f'<div class="content-callout callout callout-{callout_type}">'
                        f"<strong>{_escape(display_title)}</strong> {inner_html}</div>"
                    )
                else:
                    # Legacy string rendering
                    callout_content = render_inline_links(
                        self._apply_dt(content),
                        site=self.site,
                        current_page=self.page,
                        ipfs=getattr(self, "ipfs", False),
                        renderer=self,
                    )
                    return (
                        f'<div class="content-callout callout callout-{callout_type}">'
                        f"<strong>{_escape(display_title)}</strong> {callout_content}</div>"
                    )

        # Render Code Blocks
        if "code" in block:
            code_data = block["code"]
            code_text = _escape(code_data.get("text", ""))
            code_lang = _escape(code_data.get("lang", ""))
            return (
                f"<pre class='content-pre'><code class='content-code language-{code_lang}'>"
                f"{code_text}</code></pre>"
            )

        # Render Unordered Lists
        if "ul" in block:
            return self._render_list_html(block["ul"], ordered=False)

        # Render Ordered Lists
        if "ol" in block:
            return self._render_list_html(block["ol"], ordered=True)

        # Render Tables
        if "table" in block:
            return self._render_table(block["table"])

        # Render Horizontal Rules
        if "hr" in block:
            return "<hr class='content-hr'>"

        return ""

    def _render_list_html(self, items: list[Any], ordered: bool) -> str:
        """Renders a list (ordered or unordered) recursively."""
        tag = "ol" if ordered else "ul"
        css_class = f"content-{tag}"
        html_parts = [f"<{tag} class='{css_class}'>"]

        for item in items:
            # Handle Task List Items
            is_task = False
            is_checked = False
            item_content = item

            if isinstance(item, dict) and item.get("task"):
                is_task = True
                is_checked = item.get("checked", False)
                # Remove task metadata from content to avoid rendering it
                item_content = item.copy()
                item_content.pop("task", None)
                item_content.pop("checked", None)
                # If only 'p' remains, extract it for simpler rendering
                if len(item_content) == 1 and "p" in item_content:
                    item_content = item_content["p"]

            li_class = "content-li"
            if is_task:
                li_class += " task-list-item"

            html_parts.append(f"<li class='{li_class}'>")

            if is_task:
                checked_attr = 'checked="checked"' if is_checked else ""
                html_parts.append(
                    f'<input type="checkbox" class="task-list-item-checkbox" disabled="disabled" {checked_attr}> '
                )

            if isinstance(item_content, str):
                # Simple string item
                html_parts.append(
                    render_inline_links(
                        self._apply_dt(item_content),
                        site=self.site,
                        current_page=self.page,
                        ipfs=getattr(self, "ipfs", False),
                        renderer=self,
                    )
                )
            elif isinstance(item_content, dict):
                # Complex item (nested list or paragraphs)
                # If it has 'p', render it
                if "p" in item_content:
                    html_parts.append(
                        render_inline_links(
                            self._apply_dt(item_content["p"]),
                            site=self.site,
                            current_page=self.page,
                            ipfs=getattr(self, "ipfs", False),
                            renderer=self,
                        )
                    )

                # Check for nested lists
                if "ul" in item_content:
                    html_parts.append(
                        self._render_list_html(item_content["ul"], ordered=False)
                    )
                if "ol" in item_content:
                    html_parts.append(
                        self._render_list_html(item_content["ol"], ordered=True)
                    )

            html_parts.append("</li>")

        html_parts.append(f"</{tag}>")
        return "".join(html_parts)

    def _render_table(self, table_data: dict[str, Any]) -> str:
        """Renders a table."""
        headers = table_data.get("headers", [])
        rows = table_data.get("rows", [])

        html_parts = ["<div class='table-wrapper'><table class='content-table'>"]

        # Render Headers
        if headers:
            html_parts.append("<thead><tr>")
            for header in headers:
                html_parts.append(
                    f"<th>{render_inline_links(self._apply_dt(header), site=self.site, current_page=self.page, ipfs=getattr(self, 'ipfs', False), renderer=self)}</th>"
                )
            html_parts.append("</tr></thead>")

        # Render Body
        html_parts.append("<tbody>")
        for row in rows:
            html_parts.append("<tr>")
            for cell in row:
                html_parts.append(
                    f"<td>{render_inline_links(self._apply_dt(cell), site=self.site, current_page=self.page, ipfs=getattr(self, 'ipfs', False), renderer=self)}</td>"
                )
            html_parts.append("</tr>")
        html_parts.append("</tbody>")

        html_parts.append("</table></div>")
        return "".join(html_parts)

    def render_blocks(
        self,
        blocks: list[dict[str, Any]],
        title: str | None = None,
        description: str | None = None,
        creation_date: str | None = None,
        creation_time: str | None = None,
        modify_date: str | None = None,
        modify_time: str | None = None,
        version: str | None = None,
        site: Any = None,
        page: Any = None,
        toc: str | None = None,
        footnotes: dict[str, str] | None = None,
        ipfs: bool = False,
        host: str = "localhost",
        port: int = 70,
        **kwargs,
    ) -> str:
        """Renders a list of blocks to HTML."""
        super().render_blocks(
            blocks,
            title,
            description,
            creation_date,
            creation_time,
            modify_date,
            modify_time,
            version,
            site,
            page,
            toc,
            footnotes,
            ipfs,
            **kwargs,
        )

        html_output = []
        for block in blocks:
            html_output.append(self.render_block(block))

        # Append footnotes if any
        if self.footnotes:
            html_output.append(render_footnotes(self.footnotes))

        final_html = "\n".join(html_output)

        # Post-process to link footnote references
        final_html = replace_footnote_refs(final_html)

        return final_html


class GemtextRenderer(BaseRenderer):
    """Renders a list of Markdown block dictionaries into Gemtext format."""

    def render_blocks(
        self,
        blocks: list[dict[str, Any]],
        title: str | None = None,
        description: str | None = None,
        creation_date: str | None = None,
        creation_time: str | None = None,
        modify_date: str | None = None,
        modify_time: str | None = None,
        version: str | None = None,
        site: Any = None,
        page: Any = None,
        toc: str | None = None,
        footnotes: dict[str, str] | None = None,
        ipfs: bool = False,
        host: str = "localhost",
        port: int = 70,
        **kwargs,
    ) -> str:
        """Produces a Gemtext string from Markdown blocks."""
        super().render_blocks(
            blocks,
            title,
            description,
            creation_date,
            creation_time,
            modify_date,
            modify_time,
            version,
            site,
            page,
            toc,
            footnotes,
            ipfs,
            **kwargs,
        )

        rendered_lines: list[str] = []

        # Helper function to recursively render list items for Gemtext.
        def _render_list(list_items, indent: int = 0, is_ordered: bool = False):
            output_lines: list[str] = []
            for item_index, item_data in enumerate(list_items, start=1):
                # Gemtext lists are always unordered (*).
                # We can simulate indentation or ordering with text, but standard Gemtext is just *.
                # Let's stick to simple * for now, or maybe use numbers for ordered.
                prefix = "* "
                if is_ordered:
                    prefix = f"{item_index}. "

                # Handle plain string list items.
                if isinstance(item_data, str):
                    output_lines.append(f"{prefix}{self._apply_dt(item_data)}")

                # Handle dictionary list items (can contain paragraphs and/or nested lists).
                elif isinstance(item_data, dict):
                    if "p" in item_data:
                        output_lines.append(f"{prefix}{self._apply_dt(item_data['p'])}")

                    # Recursively render nested unordered lists.
                    if "ul" in item_data:
                        output_lines.extend(
                            _render_list(
                                item_data["ul"], indent=indent + 2, is_ordered=False
                            )
                        )
                    # Recursively render nested ordered lists.
                    if "ol" in item_data:
                        output_lines.extend(
                            _render_list(
                                item_data["ol"], indent=indent + 2, is_ordered=True
                            )
                        )
                else:
                    # Fallback
                    output_lines.append(f"{prefix}{self._apply_dt(str(item_data))}")
            return output_lines

        # Regex for finding links in text: [label](href)
        link_pattern = re.compile(r"\[(?P<label>[^\]]+)\]\((?P<href>[^\)]+)\)")

        # Add title and description (if provided) as headers.
        if title:
            rendered_lines.append(f"# {self._apply_dt(title)}")  # Main title
            if description:
                rendered_lines.append(
                    self._apply_dt(description)
                )  # Description below title

            # Optionally add date/time if available.
            if creation_date or creation_time:
                combined_datetime = " ".join(
                    x for x in (creation_date or "", creation_time or "") if x
                )
                if combined_datetime:
                    rendered_lines.append(combined_datetime)

        # Iterate through each parsed Markdown block to convert it to Gemtext.
        for block in blocks:
            # Render Headings (H1, H2, H3, etc.)
            if any(h_tag in block for h_tag in HEADINGS):
                for h_tag in HEADINGS:
                    if h_tag in block:
                        heading_level = int(
                            h_tag[1]
                        )  # Extract heading level (e.g., 1 from 'h1').
                        # Gemtext headings use # based on level.
                        rendered_lines.append(
                            "#" * heading_level
                            + " "
                            + self._apply_dt(str(block[h_tag]))
                        )
                        break  # Only process the first heading found in the block.

            # Render Paragraphs and Links
            elif "p" in block:
                # Apply date/time placeholders to the paragraph text.
                paragraph_text = self._apply_dt(str(block["p"]))

                # Replace tipping token
                paragraph_text = replace_tipping_token(paragraph_text, self)

                # Extract links from the paragraph to format them for Gemtext.
                extracted_links = []
                for m in link_pattern.finditer(paragraph_text):
                    label = m.group("label")
                    href = m.group("href")
                    # Resolve link
                    href = resolve_link(href, self.site, self.page, self.ipfs, self)
                    extracted_links.append((label, href))

                # Remove Markdown link syntax from the paragraph text itself.
                paragraph_text = link_pattern.sub(
                    lambda m: m.group("label"), paragraph_text
                )
                rendered_lines.append(paragraph_text)

                # Add Gemtext link lines after the paragraph.
                for link_label, link_href in extracted_links:
                    rendered_lines.append(f"=> {link_href} {link_label}")

            # Render Code Blocks
            elif "code" in block:
                code_content = block["code"].get("text", "")
                rendered_lines.append("```")  # Gemtext code block start marker.
                rendered_lines.append(code_content)
                rendered_lines.append("```")  # Gemtext code block end marker.

            # Render Unordered Lists
            elif "ul" in block:
                # Use the inner helper to render the list.
                rendered_lines.extend(
                    _render_list(block["ul"], indent=0, is_ordered=False)
                )

            # Render Ordered Lists
            elif "ol" in block:
                # Use the inner helper to render the list.
                rendered_lines.extend(
                    _render_list(block["ol"], indent=0, is_ordered=True)
                )

            # Render Images
            elif "image" in block:
                image_data = block["image"] or {}
                image_src = image_data.get("src", "")
                image_alt = self._apply_dt(image_data.get("alt", ""))
                # Gemtext links are used for images.
                rendered_lines.append(f"=> {image_src} {image_alt}")

            # Render Blockquotes
            elif "blockquote" in block:
                # Gemtext blockquotes start with '> '.
                rendered_lines.append(f"> {str(block['blockquote'])}")

        # Join all rendered lines with double newlines to separate blocks in Gemtext.
        return "\n\n".join(rendered_lines)


class GopherRenderer(BaseRenderer):
    """Renders a list of Markdown block dictionaries into a Gophermap-like plain-text format.

    Gophermap is a simple, line-oriented text format for the Gopher protocol.
    This renderer converts parsed Markdown blocks into corresponding Gophermap
    lines, which include informational lines ('i' type) and handle structured
    content like headings, paragraphs, lists, and code blocks. It also
    supports dynamic date and time placeholder replacement.
    """

    def render_blocks(
        self,
        blocks: list[dict[str, Any]],
        title: str | None = None,
        description: str | None = None,
        creation_date: str | None = None,
        creation_time: str | None = None,
        modify_date: str | None = None,
        modify_time: str | None = None,
        version: str | None = None,
        site: Any = None,
        page: Any = None,
        toc: str | None = None,
        footnotes: dict[str, str] | None = None,
        ipfs: bool = False,
        host: str = "localhost",
        port: int = 70,
        **kwargs,
    ) -> str:
        """Produces a simple, Gophermap-compliant text representation from Markdown blocks."""
        super().render_blocks(
            blocks,
            title,
            description,
            creation_date,
            creation_time,
            modify_date,
            modify_time,
            version,
            site,
            page,
            toc,
            footnotes,
            ipfs,
            **kwargs,
        )

        gopher_lines: list[str] = []
        # Add title and description (if provided) as informational Gophermap lines.
        if title:
            gopher_lines.append(f"i{self._apply_dt(title)}\t\t{host}\t{port}")
            if description:
                gopher_lines.append(f"i{self._apply_dt(description)}\t\t{host}\t{port}")

            # Optionally add date/time if available.
            if creation_date or creation_time:
                combined_datetime = " ".join(
                    x for x in (creation_date or "", creation_time or "") if x
                )
                if combined_datetime:
                    gopher_lines.append(f"i{combined_datetime}\t\t{host}\t{port}")

        # Inner helper function to recursively render list items for Gophermap.
        def _render_list(list_items, indent: int = 0, is_ordered: bool = False):
            output_lines: list[str] = []
            # Iterate through each item in the list.
            for item_index, item_data in enumerate(list_items, start=1):
                indent_prefix = " " * indent

                # Handle plain string list items.
                if isinstance(item_data, str):
                    display_text = ""
                    if is_ordered:
                        display_text = (
                            f"{indent_prefix}{item_index}. {self._apply_dt(item_data)}"
                        )
                    else:
                        display_text = f"{indent_prefix}- {self._apply_dt(item_data)}"
                    output_lines.append(f"i{display_text}\t\t{host}\t{port}")

                # Handle dictionary list items (can contain paragraphs and/or nested lists).
                elif isinstance(item_data, dict):
                    if "p" in item_data:
                        display_text = (
                            f"{indent_prefix}- {self._apply_dt(item_data['p'])}"
                        )
                        output_lines.append(f"i{display_text}\t\t{host}\t{port}")

                    # Recursively render nested unordered lists.
                    if "ul" in item_data:
                        output_lines.extend(
                            _render_list(
                                item_data["ul"], indent=indent + 2, is_ordered=False
                            )
                        )
                    # Recursively render nested ordered lists.
                    if "ol" in item_data:
                        output_lines.extend(
                            _render_list(
                                item_data["ol"], indent=indent + 2, is_ordered=True
                            )
                        )
                else:
                    # Fallback for unexpected item types, treating them as strings.
                    display_text = f"{indent_prefix}- {self._apply_dt(str(item_data))}"
                    output_lines.append(f"i{display_text}\t\t{host}\t{port}")
            return output_lines

        # Iterate through each parsed Markdown block to convert it to Gophermap.
        for block in blocks:
            # Render Paragraphs
            if "p" in block:
                # Get paragraph content, apply placeholders, and replace tabs for Gophermap compatibility.
                paragraph_display = self._apply_dt(str(block["p"])).replace("\t", " ")
                # Replace tipping token
                paragraph_display = replace_tipping_token(paragraph_display, self)
                gopher_lines.append(f"i{paragraph_display}\t\t{host}\t{port}")

            # Render H1 Headings (other headings are typically just text in Gophermap)
            elif "h1" in block:
                heading_display = "# " + self._apply_dt(str(block["h1"]))
                gopher_lines.append(f"i{heading_display}\t\t{host}\t{port}")

            # Render Unordered Lists
            elif "ul" in block:
                gopher_lines.extend(
                    _render_list(block["ul"], indent=0, is_ordered=False)
                )

            # Render Ordered Lists
            elif "ol" in block:
                gopher_lines.extend(
                    _render_list(block["ol"], indent=0, is_ordered=True)
                )

            # Render Code Blocks
            elif "code" in block:
                code_content = block["code"].get("text", "")
                # Each line of the code block is an informational Gophermap line.
                for code_line in code_content.splitlines():
                    gopher_lines.append(
                        f"i{self._apply_dt(code_line)}\t\t{host}\t{port}"
                    )

        # Gopher protocol historically expects CRLF (Carriage Return Line Feed) as line endings.
        return "\r\n".join(gopher_lines) + "\r\n"


# Backwards-compatible thin wrappers


def render_block(block: dict[str, Any]) -> str:
    """Renders a single Markdown block dictionary into its HTML string representation.

    This is a convenience wrapper that instantiates `HTMLRenderer` and calls its `render_block` method.
    It's provided for backward compatibility.

    Args:
        block: A dictionary representing a single parsed Markdown block.

    Returns:
        An HTML string for the given block.
    """

    return HTMLRenderer().render_block(block)


def render_blocks(
    blocks: list[dict[str, Any]],
    fmt: str = "html",
    title: str | None = None,
    description: str | None = None,
    date: str | None = None,
    time: str | None = None,
) -> str:
    """Renders a list of Markdown block dictionaries into a specified output format.

    This is a convenience wrapper function that dispatches the rendering task
    to the appropriate renderer class (HTMLRenderer, GemtextRenderer, or GopherRenderer)
    based on the `fmt` argument. It's provided for backward compatibility.

    Args:
        blocks: A list of dictionaries, each representing a parsed Markdown block.
        fmt: The desired output format ("html", "gemini", or "gopher"). Defaults to "html".
        title: The title of the document.
        description: A brief description of the document.
        date: The current date string for placeholder replacement.
        time: The current time string for placeholder replacement.

    Returns:
        A string representing the fully rendered document content in the specified format.
    """

    fmt_lower = (fmt or "").lower()  # Ensure format is lowercase for comparison.

    if fmt_lower == "html":
        # Render HTML using HTMLRenderer, passing all relevant metadata.
        return HTMLRenderer().render_blocks(
            blocks,
            title=title,
            description=description,
            creation_date=date,
            creation_time=time,
        )

    if fmt_lower == "gemini" or fmt_lower == "gemtext":
        # Render Gemtext using GemtextRenderer, passing relevant metadata.
        return GemtextRenderer().render_blocks(
            blocks,
            title=title,
            description=description,
            creation_date=date,
            creation_time=time,
        )

    if fmt_lower == "gopher":
        # Render Gophermap using GopherRenderer, passing relevant metadata.
        return GopherRenderer().render_blocks(
            blocks,
            title=title,
            description=description,
            creation_date=date,
            creation_time=time,
        )

    # Fallback if an unsupported format is requested.
    return "\n\n".join(str(b) for b in blocks)
