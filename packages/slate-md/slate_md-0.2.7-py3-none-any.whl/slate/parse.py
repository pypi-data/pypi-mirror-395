"""
This module is responsible for parsing Markdown text into a structured list
of dictionaries, often referred to as an Abstract Syntax Tree (AST) or
"block dicts". These block dicts represent the various elements of the
Markdown document (e.g., headings, paragraphs, lists, code blocks) in a
format that can be easily consumed by renderers.

It leverages the `markdown-it-py` library for the initial parsing into
a stream of tokens, and then further processes these tokens to create
a simplified, dictionary-based representation suitable for Slate's rendering
pipeline.
"""

import re
from typing import Any

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.tasklists import tasklists_plugin

# Define a list of recognized callout types.
# Callouts are special blocks that highlight information, warnings, etc.
CALLOUTS = ("NOTE", "WARNING", "DANGER", "SUCCESS", "TIP")


def parse_markdown_to_dicts(mdtext: str) -> list[dict[str, Any]]:
    """Parses a Markdown string into a list of block dictionaries.

    This function takes raw Markdown text, processes it using the markdown-it-py
    library, and then transforms the resulting tokens into a more semantic
    list of dictionaries. Each dictionary represents a distinct block-level
    element of the Markdown document, such as a heading, paragraph, list,
    or code block.

    Args:
        mdtext: The input Markdown text as a string.

    Returns:
        A list of dictionaries, where each dictionary represents a parsed
        block from the Markdown document.
    """
    # Initialize the MarkdownIt parser with commonmark rules.
    # 'breaks': True ensures that newline characters are treated as hard breaks.
    # 'html': True allows raw HTML to be included.
    # 'gfm-like': Enables GitHub Flavored Markdown features (tables, task lists, etc.)
    md = (
        MarkdownIt("gfm-like", {"breaks": True, "html": True, "linkify": False})
        # Enable front matter plugin to handle YAML front matter if present.
        .use(front_matter_plugin)
        # Enable tasklists plugin for GFM task lists.
        .use(tasklists_plugin)
        # Enable strikethrough (already enabled by gfm-like, but keeping for safety)
        .enable("strikethrough")
        .enable("table")
    )

    # Parse the Markdown text into a stream of tokens.
    tokens = md.parse(mdtext)

    # This list will store the final block dictionaries that represent the Markdown document.
    return parse_tokens(tokens)


def parse_tokens(tokens: list[Token], is_nested: bool = False) -> list[dict[str, Any]]:
    """Parses a list of markdown-it tokens into block dictionaries recursively.

    Args:
        tokens: A list of MarkdownIt tokens to parse.
        is_nested: A boolean indicating if we are currently parsing inside another block (e.g. blockquote).

    Returns:
        A list of dictionaries representing the parsed blocks.
    """
    result: list[dict[str, Any]] = []
    current_token_index = 0

    while current_token_index < len(tokens):
        token = tokens[current_token_index]

        if token.type == "heading_open":
            block, current_token_index = handle_heading(tokens, current_token_index)
            if block:
                result.append(block)
        elif token.type == "paragraph_open":
            block, current_token_index = handle_paragraph(
                tokens, current_token_index, is_nested
            )
            if block:
                result.append(block)
        elif token.type == "blockquote_open":
            block, current_token_index = handle_blockquote(tokens, current_token_index)
            if block:
                result.append(block)
        elif token.type == "fence":
            block, current_token_index = handle_code_block(tokens, current_token_index)
            if block:
                result.append(block)
        elif token.type in ("bullet_list_open", "ordered_list_open"):
            block, current_token_index = handle_list(tokens, current_token_index)
            if block:
                result.append(block)
        elif token.type == "table_open":
            block, current_token_index = handle_table(tokens, current_token_index)
            if block:
                result.append(block)
        elif token.type == "inline":
            # Special case: Extract images from inline tokens
            blocks, current_token_index = handle_inline_images(
                tokens, current_token_index
            )
            result.extend(blocks)
        elif token.type == "hr":
            result.append({"hr": True})
            current_token_index += 1
        else:
            current_token_index += 1

    return result


def handle_heading(
    tokens: list[Token], index: int
) -> tuple[dict[str, Any] | None, int]:
    """Handles heading tokens (h1-h6).

    Args:
        tokens: The full list of tokens.
        index: The current index pointing to 'heading_open'.

    Returns:
        A tuple containing the block dict (or None) and the new index after processing.
    """
    token = tokens[index]
    # token.tag is like 'h1', 'h2', etc.
    heading_tag = f"h{token.tag[1]}"
    # The content is in the next inline token (index + 1)
    # Structure: heading_open -> inline -> heading_close
    heading_text = (
        tokens[index + 1].content if tokens[index + 1].type == "inline" else ""
    )
    # Skip 3 tokens: open, inline, close
    return {heading_tag: heading_text}, index + 3


def handle_paragraph(
    tokens: list[Token], index: int, is_nested: bool
) -> tuple[dict[str, Any] | None, int]:
    """Handles paragraph tokens, including legacy callout syntax.

    Args:
        tokens: The full list of tokens.
        index: The current index pointing to 'paragraph_open'.
        is_nested: Whether we are inside a nested block (like a blockquote).

    Returns:
        A tuple containing the block dict (or None) and the new index after processing.
    """
    # Structure: paragraph_open -> inline -> paragraph_close
    paragraph_content = (
        tokens[index + 1].content if tokens[index + 1].type == "inline" else ""
    )

    # Check for legacy/simple callout syntax: [!NOTE] at start of paragraph
    # This is only supported at the top level, not nested.
    if not is_nested:
        for callout_type in CALLOUTS:
            callout_prefix = f"[!{callout_type}]"
            if paragraph_content.strip().upper().startswith(callout_prefix):
                # Extract content after the prefix
                stripped_content = paragraph_content.strip()[
                    len(callout_prefix) :
                ].strip()
                return {
                    f"callout-{callout_type.lower()}": [{"p": stripped_content}]
                }, index + 3

    return {"p": paragraph_content}, index + 3


def handle_blockquote(
    tokens: list[Token], index: int
) -> tuple[dict[str, Any] | None, int]:
    """Handles blockquotes and GitHub-style callouts.

    Args:
        tokens: The full list of tokens.
        index: The current index pointing to 'blockquote_open'.

    Returns:
        A tuple containing the block dict (or None) and the new index after processing.
    """
    # Extract tokens inside the blockquote to parse them recursively
    inner_tokens = []
    current_index = index + 1
    nesting_level = 1

    # Iterate until we find the matching closing tag
    while current_index < len(tokens) and nesting_level > 0:
        if tokens[current_index].type == "blockquote_open":
            nesting_level += 1
        elif tokens[current_index].type == "blockquote_close":
            nesting_level -= 1

        if nesting_level > 0:
            inner_tokens.append(tokens[current_index])
        current_index += 1

    # Recursively parse inner tokens
    inner_blocks = parse_tokens(inner_tokens, is_nested=True)

    # Check if it's a Callout (GitHub style)
    # GitHub callouts look like blockquotes starting with [!NOTE]
    if inner_blocks and "p" in inner_blocks[0]:
        first_paragraph_text = inner_blocks[0]["p"]
        for callout_type in CALLOUTS:
            callout_prefix = f"[!{callout_type}]"
            if first_paragraph_text.strip().upper().startswith(callout_prefix):
                callout_type_found = callout_type.lower()
                # Remove the prefix from the first block
                inner_blocks[0]["p"] = first_paragraph_text.strip()[
                    len(callout_prefix) :
                ].strip()
                # If first block is now empty (just the label), remove it
                if not inner_blocks[0]["p"]:
                    inner_blocks.pop(0)
                return {f"callout-{callout_type_found}": inner_blocks}, current_index

    return {"blockquote": inner_blocks}, current_index


def handle_code_block(
    tokens: list[Token], index: int
) -> tuple[dict[str, Any] | None, int]:
    """Handles fenced code blocks.

    Args:
        tokens: The full list of tokens.
        index: The current index pointing to 'fence'.

    Returns:
        A tuple containing the block dict (or None) and the new index after processing.
    """
    token = tokens[index]
    return {
        "code": {
            "text": token.content,
            "lang": token.info or "",
        }
    }, index + 1


def handle_list(tokens: list[Token], index: int) -> tuple[dict[str, Any] | None, int]:
    """Handles unordered and ordered lists.

    Args:
        tokens: The full list of tokens.
        index: The current index pointing to list open.

    Returns:
        A tuple containing the block dict (or None) and the new index after processing.
    """
    # Reuse the existing recursive list parser
    return parse_list_at(tokens, index)


def handle_table(tokens: list[Token], index: int) -> tuple[dict[str, Any] | None, int]:
    """Handles tables.

    Args:
        tokens: The full list of tokens.
        index: The current index pointing to 'table_open'.

    Returns:
        A tuple containing the block dict (or None) and the new index after processing.
    """
    table_headers: list[str] = []
    table_rows: list[list[str]] = []

    # Find table headers (thead).
    # Structure: table_open -> thead_open -> tr_open -> th_open -> inline -> th_close ... -> tr_close -> thead_close
    current_index = index + 1  # Start after 'table_open'.

    # Iterate through tokens until we close the table head
    while current_index < len(tokens) and tokens[current_index].type != "thead_close":
        if tokens[current_index].type == "th_open":
            # The content is in the next inline token
            table_headers.append(tokens[current_index + 1].content)
        current_index += 1

    # Find table rows (tbody).
    # Structure: tbody_open -> tr_open -> td_open -> inline -> td_close ... -> tr_close -> tbody_close
    current_index = current_index + 1  # Start after 'thead_close'.

    # Iterate through tokens until we close the table
    while current_index < len(tokens) and tokens[current_index].type != "table_close":
        if tokens[current_index].type == "td_open":
            current_row_cells = []
            current_index += 1
            # Iterate through the row until it closes
            while (
                current_index < len(tokens) and tokens[current_index].type != "tr_close"
            ):
                if tokens[current_index].type == "inline":
                    current_row_cells.append(tokens[current_index].content)
                current_index += 1
            table_rows.append(current_row_cells)
        else:
            current_index += 1

    return {"table": {"headers": table_headers, "rows": table_rows}}, current_index + 1


def handle_inline_images(
    tokens: list[Token], index: int
) -> tuple[list[dict[str, Any]], int]:
    """Extracts images from inline tokens.

    Args:
        tokens: The full list of tokens.
        index: The current index pointing to 'inline'.

    Returns:
        A tuple containing a list of image blocks and the new index after processing.
    """
    token = tokens[index]
    blocks = []
    # Images are often children of inline tokens
    for child_token in getattr(token, "children", []):
        if child_token.type == "image":
            blocks.append(
                {
                    "image": {
                        "src": child_token.attrs.get("src", ""),
                        "alt": child_token.attrs.get("alt", ""),
                        "caption": child_token.attrs.get("title", ""),
                    }
                }
            )
    return blocks, index + 1


def parse_list_at(tokens: list[Token], start_index: int) -> tuple[dict[str, Any], int]:
    """Parses a bullet or ordered list block starting at the given token index.

    This is a recursive helper function that processes a list and its nested
    sub-lists.

    Args:
        tokens: The full list of tokens.
        start_index: The index where the list starts.

    Returns:
        A tuple containing the list dict and the new index after processing.
    """
    start_token = tokens[start_index]
    is_ordered = start_token.type == "ordered_list_open"
    list_key = "ol" if is_ordered else "ul"

    items: list[Any] = []
    current_index = start_index + 1
    close_type = "ordered_list_close" if is_ordered else "bullet_list_close"

    while current_index < len(tokens) and tokens[current_index].type != close_type:
        current_token = tokens[current_index]

        if current_token.type == "list_item_open":
            item_text = None
            nested_list_data = None
            inline_token_node = None

            # Scan inside the list item
            inner_index = current_index + 1
            while (
                inner_index < len(tokens)
                and tokens[inner_index].type != "list_item_close"
            ):
                item_content_token = tokens[inner_index]

                if item_content_token.type == "paragraph_open":
                    # Check if the next token is inline content
                    if (
                        inner_index + 1 < len(tokens)
                        and tokens[inner_index + 1].type == "inline"
                    ):
                        item_text = tokens[inner_index + 1].content
                        inline_token_node = tokens[inner_index + 1]
                        inner_index += 2
                        continue
                    inner_index += 1
                elif item_content_token.type in (
                    "bullet_list_open",
                    "ordered_list_open",
                ):
                    # Found a nested list, recurse!
                    nested_list_data, new_inner_index = parse_list_at(
                        tokens, inner_index
                    )
                    inner_index = new_inner_index
                    continue
                else:
                    inner_index += 1

            # Construct the item representation
            item_representation: Any
            if nested_list_data and item_text:
                item_representation = {"p": item_text}
                item_representation.update(nested_list_data)
            elif nested_list_data:
                item_representation = nested_list_data
            else:
                item_representation = item_text or ""

            # Handle Task Lists (GFM)
            # The tasklists plugin adds 'class': 'task-list-item' to attrs
            # and inserts an html_inline token with the checkbox at the start of the inline token's children.
            if current_token.attrs:
                class_value = current_token.attrs.get("class", "")
                if isinstance(class_value, str) and "task-list-item" in class_value:
                    is_checked = False
                    # Check the captured inline token for the checkbox HTML
                    if (
                        inline_token_node
                        and inline_token_node.children
                        and inline_token_node.children[0].type == "html_inline"
                        and 'type="checkbox"' in inline_token_node.children[0].content
                    ):
                        first_child = inline_token_node.children[0]
                        if (
                            'checked="checked"' in first_child.content
                            or "checked " in first_child.content
                        ):
                            is_checked = True

                    if isinstance(item_representation, str):
                        item_representation = {"p": item_representation}

                    if isinstance(item_representation, dict):
                        item_representation["task"] = True
                        item_representation["checked"] = is_checked

            items.append(item_representation)
            current_index = inner_index + 1
        else:
            current_index += 1

    return ({list_key: items}, current_index + 1)


def generate_toc(blocks: list[dict[str, Any]]) -> str:
    """Generate table of contents HTML from heading blocks.

    Args:
        blocks: The parsed block dictionaries.

    Returns:
        An HTML string representing the Table of Contents.
    """
    toc_items = []

    for block in blocks:
        for level_key in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            if level_key in block:
                text = block[level_key]
                level = int(level_key[1])
                slug = slugify(text)
                toc_items.append({"level": level, "text": text, "slug": slug})
                break

    if not toc_items:
        return ""

    html_lines = ['<nav class="toc">', "  <ul>"]

    for item in toc_items:
        level_class = f' class="toc-h{item["level"]}"' if item["level"] > 1 else ""
        html_lines.append(
            f'    <li{level_class}><a href="#{item["slug"]}">{item["text"]}</a></li>'
        )

    html_lines.extend(["  </ul>", "</nav>"])

    return "\n".join(html_lines)


def slugify(text: str) -> str:
    """Convert text to URL-safe slug.

    Args:
        text: The input string to slugify.

    Returns:
        A URL-safe slug string.
    """
    slug = text.lower()
    # REGEX: Remove any character that is NOT a word character (\w), whitespace (\s), or hyphen (-).
    # This effectively strips punctuation and special characters.
    slug = re.sub(r"[^\w\s-]", "", slug)

    # REGEX: Replace one or more occurrences of hyphens or whitespace ([-\s]+) with a single hyphen.
    # This ensures we don't have multiple hyphens in a row (e.g., "foo--bar" -> "foo-bar").
    slug = re.sub(r"[-\s]+", "-", slug)

    return slug.strip("-")


def parse_footnotes(md_text: str) -> tuple[str, dict[str, str]]:
    """Parse footnotes from Markdown text.

    Args:
        md_text: The raw Markdown text.

    Returns:
        A tuple containing the text with footnotes removed, and a dictionary of footnote ID -> text.
    """
    # REGEX: Match footnote definitions at the start of a line.
    # ^           : Start of the line
    # \[\^        : Literal "[^"
    # (\w+)       : Capture group 1: The footnote ID (one or more word characters)
    # \]          : Literal "]"
    # :           : Literal ":"
    # \s*         : Zero or more whitespace characters
    # (.+)        : Capture group 2: The footnote text (rest of the line)
    # $           : End of the line
    footnote_pattern = r"^\[\^(\w+)\]:\s*(.+)$"
    footnotes = {}
    lines = []

    for line in md_text.split("\n"):
        match = re.match(footnote_pattern, line)
        if match:
            footnote_id = match.group(1)
            footnote_text = match.group(2).strip()
            footnotes[footnote_id] = footnote_text
        else:
            lines.append(line)

    return "\n".join(lines), footnotes


def render_footnotes(footnotes: dict[str, str]) -> str:
    """Render footnotes as HTML.

    Args:
        footnotes: A dictionary of footnote ID -> text.

    Returns:
        An HTML string representing the footnotes section.
    """
    if not footnotes:
        return ""

    html_lines = ['<div class="footnotes">', "  <hr>", "  <ol>"]

    for key, text in sorted(footnotes.items()):
        html_lines.append(
            f'    <li id="fn-{key}">{text} <a href="#fnref-{key}" class="footnote-backref">↩</a></li>'
        )

    html_lines.extend(["  </ol>", "</div>"])

    return "\n".join(html_lines)


def replace_footnote_refs(html: str) -> str:
    """Replace footnote reference markers with HTML links.

    Args:
        html: The HTML string containing footnote references like [^1].

    Returns:
        The HTML string with references replaced by links.
    """

    def replace_fn_ref(match):
        footnote_id = match.group(1)
        return f'<sup><a href="#fn-{footnote_id}" id="fnref-{footnote_id}" class="footnote-ref">[{footnote_id}]</a></sup>'

    # REGEX: Match footnote references in the text.
    # \[\^        : Literal "[^"
    # (\w+)       : Capture group 1: The footnote ID (one or more word characters)
    # \]          : Literal "]"
    return re.sub(r"\[\^(\w+)\]", replace_fn_ref, html)
