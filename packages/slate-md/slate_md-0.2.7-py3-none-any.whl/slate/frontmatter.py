"""Frontmatter parsing and validation for Slate.

This module handles YAML frontmatter extraction from Markdown files,
providing metadata for site management features in v0.2.0.

Frontmatter format:
---
title: My Post
description: A great post
template: blog.html
category: blog
type: blog  # or "page"
date: 2024-12-01
author: Author Name
---
"""

import re
from datetime import datetime
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise ImportError(
        "PyYAML is required for frontmatter support. "
        "Install with: pip install pyyaml"
    ) from exc


def extract_frontmatter(md_text: str) -> tuple[dict[str, Any], str]:
    """Extract YAML frontmatter from Markdown text.
    
    Frontmatter is optional metadata at the top of a Markdown file, like this:
    ---
    title: My Post
    description: A great post
    ---
    
    # Your content here...
    
    Args:
        md_text: The full Markdown text, potentially with frontmatter.
        
    Returns:
        A tuple of (metadata_dict, markdown_content).
        If no frontmatter is found, returns ({}, original_text).
        
    Raises:
        ValueError: If frontmatter YAML is invalid.
    """
    # === REGEX PATTERN EXPLANATION ===
    # This pattern matches frontmatter in this format:
    # ---
    # yaml content here
    # ---
    # markdown content here
    #
    # Pattern breakdown:
    # ^---\s*\n     = Start of file, then "---", optional whitespace, then newline
    # (.*?)         = Capture group 1: YAML content (non-greedy, stops at first match)
    # \n---\s*\n    = Newline, "---", optional whitespace, newline (closing delimiter)
    # (.*)$         = Capture group 2: Everything after (the Markdown content)
    #
    # re.DOTALL flag makes "." match newlines too (so we can capture multi-line content)
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(frontmatter_pattern, md_text, re.DOTALL)
    
    if not match:
        # No frontmatter found - that's okay! It's optional.
        return {}, md_text
    
    # Extract the two captured groups from our regex match
    yaml_content = match.group(1)     # Everything between the --- markers
    markdown_content = match.group(2)  # Everything after the closing ---
    
    # Parse the YAML content into a Python dictionary
    try:
        metadata = yaml.safe_load(yaml_content)
        # Handle edge case: empty frontmatter (just "---\n---")
        if metadata is None:
            metadata = {}
    except yaml.YAMLError as e:
        # If the YAML is malformed, give a helpful error message
        raise ValueError(f"Invalid frontmatter YAML: {e}") from e
    
    return metadata, markdown_content


def validate_frontmatter(metadata: dict[str, Any], file_path: str) -> list[str]:
    """Validate frontmatter fields based on type and requirements.
    
    Args:
        metadata: The frontmatter dictionary to validate.
        file_path: Path to the file (for error messages).
        
    Returns:
        List of validation error messages. Empty list if valid.
    """
    errors = []
    
    # If type is "blog", require date and title
    if metadata.get("type") == "blog":
        if "date" not in metadata:
            errors.append(f"{file_path}: Blog posts require 'date' field")
        else:
            # YAML parses dates as datetime.date objects, which is fine
            # Also accept strings in ISO format
            date_value = metadata["date"]
            if isinstance(date_value, str):
                try:
                    datetime.fromisoformat(date_value)
                except ValueError:
                    errors.append(
                        f"{file_path}: 'date' must be in ISO format (YYYY-MM-DD), "
                        f"got: {date_value}"
                    )
            elif not isinstance(date_value, datetime):
                # datetime.date is a subclass of datetime for isinstance checks
                # Actually datetime.date is NOT a subclass, need to import date
                from datetime import date as date_type
                if not isinstance(date_value, (datetime, date_type)):
                    errors.append(
                        f"{file_path}: 'date' must be a date string or datetime object, "
                        f"got: {type(date_value).__name__}"
                    )
        
        if "title" not in metadata:
            errors.append(f"{file_path}: Blog posts require 'title' field")
    
    # Validate date format if present (only for string dates not already checked above)
    # YAML auto-parses dates to datetime.date objects, which are already validated above
    
    # Validate type field if present
    if "type" in metadata:
        valid_types = ["blog", "page"]
        if metadata["type"] not in valid_types:
            errors.append(
                f"{file_path}: 'type' must be one of {valid_types}, "
                f"got: {metadata['type']}"
            )
    
    # Validate category is a string if present
    if "category" in metadata and not isinstance(metadata["category"], str):
        errors.append(f"{file_path}: 'category' must be a string")
    
    return errors


def merge_with_cli_args(frontmatter: dict[str, Any], cli_args: dict[str, Any]) -> dict[str, Any]:
    """Merge frontmatter with CLI arguments, with frontmatter taking precedence.
    
    Args:
        frontmatter: Metadata from frontmatter.
        cli_args: Arguments from command line.
        
    Returns:
        Merged dictionary with frontmatter values overriding CLI where present.
    """
    merged = cli_args.copy()
    
    # Frontmatter takes precedence for these fields
    for key in ["title", "description", "template"]:
        if key in frontmatter:
            merged[key] = frontmatter[key]
    
    return merged
