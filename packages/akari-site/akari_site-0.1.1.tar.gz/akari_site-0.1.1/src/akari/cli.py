# ABOUTME: CLI tool for Akari static site generator
# ABOUTME: Contains all build logic and CLI commands in a single file

import click
import shutil
from pathlib import Path
from datetime import datetime
import yaml
import markdown
from importlib import resources
from watchfiles import watch as watch_for_changes
import time


# === BUILDER FUNCTIONS ===

def load_template(template_name, templates_dir):
    """Load a template file from templates directory."""
    template_path = Path(templates_dir) / template_name
    with open(template_path, "r") as f:
        return f.read()


def load_section_template(section, template_name, templates_dir):
    """Load a template for a specific section."""
    template_path = Path(templates_dir) / section / template_name
    with open(template_path, "r") as f:
        return f.read()


def parse_markdown_file(file_path):
    """Parse markdown file with YAML front matter."""
    with open(file_path, "r") as f:
        content = f.read()

    # Split on first two --- delimiters
    parts = content.split("---", 2)
    front_matter_str = parts[1]
    markdown_content = parts[2]

    # Parse YAML and markdown
    metadata = yaml.safe_load(front_matter_str)
    html_content = markdown.markdown(markdown_content)

    # Extract slug from filename (YYYY-MM-DD-slug.md -> slug)
    filename = Path(file_path).stem
    slug_parts = filename.split("-", 3)
    slug = slug_parts[3] if len(slug_parts) >= 4 else filename

    # Parse date if it's in string format
    date = metadata["date"]
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d")

    return {
        "title": metadata["title"],
        "date": date,
        "content": html_content,
        "slug": slug,
        "path": file_path
    }


def load_posts(directory):
    """Load all posts from a directory."""
    posts = []
    path = Path(directory)

    if not path.exists():
        return posts

    for file_path in sorted(path.glob("*.md")):
        try:
            post = parse_markdown_file(file_path)
            posts.append(post)
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

    # Sort by date (newest first)
    posts.sort(key=lambda x: x["date"], reverse=True)
    return posts


def format_date(date_obj):
    """Format date for display."""
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime("%B %d, %Y")


def discover_sections(content_dir):
    """Discover all sections by scanning content/ subdirectories."""
    content_path = Path(content_dir)
    sections = []
    for item in sorted(content_path.iterdir()):
        if item.is_dir():
            sections.append(item.name)
    return sections


def generate_navigation(sections):
    """Generate navigation HTML from discovered sections."""
    nav_items = []
    for section in sections:
        display_name = section.capitalize()
        nav_items.append(f'<li><a href="/{section}/">{display_name}</a></li>')
    return '\n                '.join(nav_items)


def render_page(template_section, template_name, title, navigation, templates_dir, **context):
    """
    Generic page renderer.

    Args:
        template_section: Section name (e.g., 'posts') or None for no template
        template_name: Template file name (e.g., 'item.html', 'index.html') or None
        title: Page title (used for <title> tag)
        navigation: Navigation HTML
        templates_dir: Path to templates directory
        **context: Additional context variables for template
    """
    # Load section-specific template if specified
    if template_section and template_name:
        template = load_section_template(template_section, template_name, templates_dir)
        # Ensure title is in context for template rendering
        context['title'] = context.get('title', title)
        content = template.format(**context)
    else:
        # Direct content (for about page)
        content = context.get('content', '')

    # Wrap with base template
    base_template = load_template("base.html", templates_dir)
    return base_template.format(
        title=title,
        content=content,
        navigation=navigation
    )


def copy_static_assets(static_dir, output_dir):
    """Copy static assets to site directory."""
    src = Path(static_dir)
    dst = Path(output_dir) / "static"

    # Remove existing static directory if it exists
    if dst.exists():
        shutil.rmtree(dst)

    # Copy entire static directory
    shutil.copytree(src, dst)


def ensure_dir(directory):
    """Ensure directory exists."""
    Path(directory).mkdir(parents=True, exist_ok=True)


def build_site(source_dir="."):
    """Build the entire static site."""
    source = Path(source_dir)
    print("Building static site...")

    content_dir = source / "content"
    templates_dir = source / "templates"
    output_dir = source / "dist"
    static_dir = source / "static"

    # Discover sections dynamically
    sections = discover_sections(content_dir)

    # Generate navigation HTML
    nav_html = generate_navigation(sections)

    # Process each section
    for section in sections:
        print(f"Processing section: {section}")

        # Load all items in this section
        items = load_posts(content_dir / section)

        # Ensure output directory exists
        ensure_dir(output_dir / section)

        # Generate individual item pages
        for item in items:
            html = render_page(
                template_section=section,
                template_name='item.html',
                title=item['title'],
                navigation=nav_html,
                templates_dir=templates_dir,
                date=format_date(item['date']),
                content=item['content']
            )
            output_path = Path(output_dir) / section / f"{item['slug']}.html"
            with open(output_path, "w") as f:
                f.write(html)
            print(f"  Generated {output_path}")

        # Generate section index page
        if items:
            # Build post list HTML
            post_items = []
            for item in items:
                link = f"/{section}/{item['slug']}.html"
                date_str = format_date(item['date'])
                post_items.append(
                    f'<li><a href="{link}">{item["title"]}</a>'
                    f'<span class="post-item-date">{date_str}</span></li>'
                )
            posts_html = '\n        '.join(post_items)

            # Render index page
            display_name = section.capitalize()
            html = render_page(
                template_section=section,
                template_name='index.html',
                title=display_name,
                navigation=nav_html,
                templates_dir=templates_dir,
                posts=posts_html
            )
            with open(output_dir / section / "index.html", "w") as f:
                f.write(html)
            print(f"  Generated {output_dir / section / 'index.html'}")

    # Generate about page (special case - no section template)
    about_path = content_dir / "about.md"
    if about_path.exists():
        with open(about_path, "r") as f:
            content = f.read()
        html_content = markdown.markdown(content)

        html = render_page(
            template_section=None,
            template_name=None,
            title="About",
            navigation=nav_html,
            templates_dir=templates_dir,
            content=html_content
        )
        with open(output_dir / "index.html", "w") as f:
            f.write(html)
        print("Generated site/index.html")

    # Copy static assets
    copy_static_assets(static_dir, output_dir)
    print("Copied static assets")

    print("Build complete!")

def validate_site_structure(current_dir):
    """Validate that content/ and templates/ directories exist. Returns True if valid."""
    if not (current_dir / "content").exists():
        click.echo("Error: content/ directory not found", err=True)
        click.echo("Hint: Run 'akari init' first", err=True)
        return False

    if not (current_dir / "templates").exists():
        click.echo("Error: templates/ directory not found", err=True)
        click.echo("Hint: Run 'akari init' first", err=True)
        return False

    return True

# === SCAFFOLD FUNCTIONS ===

def init_blog(target_dir):
    """Initialize new blog by copying scaffold."""
    target = Path(target_dir)
    target.mkdir(parents=True, exist_ok=True)

    # Get scaffold directory from package
    scaffold_dir = resources.files('akari') / 'scaffold'

    # Copy everything
    for item in scaffold_dir.iterdir():
        if item.is_dir():
            shutil.copytree(item, target / item.name, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target / item.name)

    print(f"✓ Initialized new blog in {target}")
    print("\nNext steps:")
    print(f"  cd {target}")
    print("  # Add posts to content/posts/")
    print("  akari build")


# === CLI COMMANDS ===

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Akari - minimalist static site generator"""
    pass


@cli.command()
@click.argument('directory', required=False, default='.')
def init(directory):
    """Initialize a new blog in DIRECTORY"""
    init_blog(directory)



@cli.command()
def build():
    """Build the static site from current directory"""
    current_dir = Path.cwd()

    if not validate_site_structure(current_dir):
        return

    build_site(current_dir)


@cli.command()
def watch():
    """Watch for changes and rebuild the site automatically"""
    current_dir = Path.cwd()

    if not validate_site_structure(current_dir):
        return

    # Initial build
    build_site(current_dir)

    click.echo("✓ Watching for changes... (Press Ctrl+C to stop)")

    try:
        for changes in watch_for_changes(current_dir / "content", current_dir / "templates", current_dir / "static"):
            click.echo(f"\n✓ Changes detected")
            click.echo("Rebuilding site...")

            try:
                build_site(current_dir)
                click.echo("✓ Rebuild complete. Watching for changes...\n")
            except Exception as e:
                click.echo(f"✗ Build failed: {e}\n", err=True)
    except KeyboardInterrupt:
        click.echo("\n✓ Watch mode stopped")


if __name__ == '__main__':
    cli()
