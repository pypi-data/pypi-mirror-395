# akari
[![PyPI](https://img.shields.io/pypi/v/hikugen?style=flat-square&logo=pypi)](https://pypi.org/project/akari-site/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A minimalist static site generator.

## Installation

```bash
uv tool install akari-site
```

## Quick Start

```bash
# Initialize new blog
akari init my-blog
cd my-blog

# Build
akari build

# Or use watch mode for development
akari watch

# Output is in dist/
```

## Features

- **Zero framework bloat** - just Python, YAML, and Markdown
- **Dynamic sections** - any folder in `content/` becomes a section
- **Section-specific templates** - customize each section's design
- **Auto-generated navigation** - nav builds from discovered sections
- **GitHub Pages ready** - outputs pure static HTML to `dist/`

## Using Your Blog

### Add Posts

Create files in `content/posts/` with YAML front matter:

```markdown
---
title: "My First Post"
date: 2025-11-30
---

Your content here...
```

### Create New Sections

1. Create `content/my-section/` with Markdown files
2. Create `templates/my-section/` with `item.html` and `index.html`
3. Run `akari build`

### Build

```bash
akari build
```

Output is in `dist/`. Deploy to GitHub Pages!

### Watch for Changes

During development, use watch mode to automatically rebuild when you change files:

```bash
akari watch
```

This will:
- Perform an initial build
- Watch `content/` and `templates/` directories for changes
- Automatically rebuild when any files change
- Press Ctrl+C to stop watching

Perfect for development - just save your changes and the site rebuilds automatically!

## Project Structure

```
my-blog/
├── content/
│   ├── about.md
│   ├── posts/
│   │   └── 2025-11-30-hello.md
│   └── projects/
├── templates/
│   ├── base.html
│   ├── posts/
│   │   ├── item.html
│   │   └── index.html
│   └── projects/
│       ├── item.html
│       └── index.html
└── static/
    ├── css/style.css
    ├── logo.svg
    └── favicon.ico
```

## Development

```bash
git clone <repo>
cd akari
uv sync
uv tool install .
```

To test locally:

```bash
akari init test-blog
cd test-blog
akari build
python -m http.server --directory dist 8000
```
