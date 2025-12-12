# Slate

> **KISS, reliable, and accessible.**

Slate is a lightweight Python CLI tool for converting Markdown to accessible static HTML pages, Gemtext, and Gophermaps. Designed for blogs, knowledge bases, and personal sites where simplicity is paramount.

## Features

- **Semantic HTML**: Converts Markdown to accessible HTML5 with semantic tags.
- **Multi-Format**: Outputs to HTML, Gemini (Gemtext), and Gopher.
- **Smart Updates**: intelligently updates existing files without needing to re-specify arguments.
- **Dynamic Links**: Automatically converts `[!MD-PAGE]` links to `.html` in the output, keeping your Markdown portable.
- **Customizable**: Integrates with Jinja2 templates and outputs CSS-ready classes.
- **Extensible**: Easily add custom Markdown tokens via a registry system.

## Quickstart

### Install via pipx (recommended)

```bash
pipx install slate-md
```

### Or, with pip:

```bash
pip install slate-md
```

## Usage

### Build a new page

```bash
slate build <input> <output> [flags]
```

- `input`: Input Markdown file path.
- `output`: Output file path (e.g., `pages/post.html`).
- `-f, --format`: Output format: `html` (default), `gemini`, or `gopher`.
- `-T, --template`: Jinja2 HTML template file (required for `html` output).
- `-t, --title`: Optional title override; otherwise the first H1 is used.
- `-d, --description`: Optional meta description for the template.

### Update an existing page

Slate remembers the source file and template used to generate an HTML file.

```bash
slate update <output_file>
```

- `output_file`: The existing HTML file to update.

You can still override the input or template if needed:
```bash
slate update output.html input.md -T new_template.html
```

### Site Management (v0.2.0+)

Slate can now manage multi-page sites with auto-generated navigation and RSS feeds!

Create an `index.md` with categories:
```yaml
---
categories: [blog, projects]
title: My Site
url: https://example.com
template: templates/default.html
---

Welcome to my site!
```

Create category root pages (`blog.md`, `projects.md`) and organize pages in directories:
```
your-site/
├── index.md
├── blog.md
├── blog/
│   ├── post1.md
│   └── post2.md
├── projects.md
└── projects/
    └── my-project.md
```

Then rebuild your entire site:
```bash
slate rebuild
```

This will:
- Build all pages with auto-generated navigation
- Generate RSS feeds for blog categories  
- Create table of contents from headings
- Apply consistent templates across your site

### Frontmatter (v0.2.0+)

Add YAML frontmatter to your Markdown files:

```yaml
---
title: My Blog Post
description: A great post about things
template: templates/blog.html
category: blog
type: blog  # or "page"
date: 2024-12-01
author: Your Name
---

# Your content here
```

Frontmatter takes precedence over CLI arguments when both are present.

### Dynamic Links

Slate supports "Dynamic Links" to keep your Markdown navigable on GitHub/Obsidian but working correctly on your site.

Use the `[!MD-PAGE]` token:
```markdown
Check out my [!MD-PAGE] [Latest Post](posts/latest.md)
```
Slate converts this to:
```html
Check out my <a href="posts/latest.html" class="content-link">Latest Post</a>
```

### Template Variables

Your Jinja2 templates have access to these variables:

| Variable | Description |
| :--- | :--- |
| `{{ content }}` | The rendered content (HTML, Gemtext, or Gopher). |
| `{{ title }}` | The page title. |
| `{{ description }}` | The page description. |
| `{{ creation_date }}` | Original creation date (persisted in metadata). |
| `{{ creation_time }}` | Original creation time (persisted in metadata). |
| `{{ modify_date }}` | Last modification date. |
| `{{ modify_time }}` | Last modification time. |
| `{{ version }}` | Slate version. |
| `{{ nav_header }}` | **v0.2.0+** Header navigation (links to categories). |
| `{{ nav_category }}` | **v0.2.0+** Category navigation (links to pages). |
| `{{ category_name }}` | **v0.2.0+** Current category name. |
| `{{ breadcrumbs }}` | **v0.2.0+** Breadcrumb navigation. |
| `{{ toc }}` | **v0.2.0+** Auto-generated table of contents. |

## Why Slate?

Slate was created because many SSGs are needlessly complicated for me. Slate is a tiny tool that does one thing well: converts Markdown into accessible HTML (and other formats) using a template.

- **No Config Files**: Everything is CLI arguments or embedded metadata.
- **Monolithic CSS**: Designed to be used with a single CSS file.
- **Hackable**: The codebase is small and easy to extend. See `documentation/hacking` for details.

## Documentation

- [Architecture Guide](documentation/hacking/humans/architecture.md)
- [Codebase Context](documentation/hacking/machines/codebase_context.md)

## License

[LGPL v3](https://www.gnu.org/licenses/lgpl-3.0.html#license-text)
