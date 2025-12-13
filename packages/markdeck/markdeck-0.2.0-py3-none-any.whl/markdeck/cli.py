"""Command-line interface for MarkDeck."""

import sys
import webbrowser
from pathlib import Path

import click
import uvicorn

from markdeck import __version__
from markdeck.server import app, enable_watch_mode, set_presentation_file


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show version and exit')
@click.pass_context
def main(ctx, version):
    """MarkDeck - A lightweight markdown presentation tool."""
    if version:
        click.echo(f"MarkDeck version {__version__}")
        sys.exit(0)
    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
@click.argument('file', type=click.Path(exists=True, path_type=Path))
@click.option('--port', '-p', default=8000, help='Port to run the server on', type=int)
@click.option('--host', '-h', default='127.0.0.1', help='Host to bind to')
@click.option('--no-browser', is_flag=True, help='Do not open browser automatically')
@click.option('--watch', '-w', is_flag=True, help='Watch file for changes and reload automatically')
def present(file: Path, port: int, host: str, no_browser: bool, watch: bool):
    """
    Start presenting a markdown file.

    Example: markdeck present my-slides.md
    """
    # Validate file
    if not file.exists():
        click.echo(f"Error: File not found: {file}", err=True)
        sys.exit(1)

    if file.suffix.lower() not in ['.md', '.markdown']:
        click.echo("Warning: File does not have .md or .markdown extension", err=True)

    # Set the presentation file
    file_path = file.resolve()
    set_presentation_file(file_path)

    # Enable watch mode if requested
    if watch:
        enable_watch_mode(True)
        click.echo("Hot reload enabled - presentation will update when file changes")

    # Build URL
    url = f"http://{host}:{port}"

    click.echo("Starting MarkDeck server...")
    click.echo(f"Presenting: {file.name}")
    click.echo(f"URL: {url}")
    click.echo("\nPress Ctrl+C to stop the server")

    # Open browser
    if not no_browser:
        click.echo("Opening browser...")
        webbrowser.open(url)

    # Run the server with file watcher if watch mode is enabled
    try:
        if watch:
            # Use uvicorn with lifespan to start file watcher
            config = uvicorn.Config(
                app,
                host=host,
                port=port,
                log_level="warning",
                access_log=False,
            )
            server = uvicorn.Server(config)

            # Start file watcher before running server
            import asyncio

            async def run_with_watcher():
                # Start the file watcher task
                watcher_task = asyncio.create_task(
                    _watch_file_async(file_path)
                )
                try:
                    await server.serve()
                except asyncio.CancelledError:
                    watcher_task.cancel()
                    raise

            asyncio.run(run_with_watcher())
        else:
            uvicorn.run(
                app,
                host=host,
                port=port,
                log_level="warning",
                access_log=False,
            )
    except KeyboardInterrupt:
        click.echo("\n\nShutting down MarkDeck server...")
        sys.exit(0)


async def _watch_file_async(file_path: Path):
    """Watch file for changes in async context."""
    from markdeck.watcher import watch_file

    await watch_file(file_path)


@main.command()
@click.argument('filename', type=click.Path(path_type=Path))
@click.option('--title', '-t', help='Presentation title')
def init(filename: Path, title: str):
    """
    Create a new presentation from a template.

    Example: markdeck init my-presentation.md
    """
    if filename.exists():
        click.confirm(f"File {filename} already exists. Overwrite?", abort=True)

    # Create template
    template_title = title or filename.stem.replace('-', ' ').replace('_', ' ').title()
    template = f"""# {template_title}

Your presentation subtitle or tagline

---

## About This Presentation

This is a sample slide created by MarkDeck.

- Edit this file to create your presentation
- Separate slides with `---`
- Use standard Markdown syntax

---

## Features

- **Simple**: Just write Markdown
- **Fast**: Lightweight and responsive
- **Beautiful**: Clean, modern design

---

## Code Examples

You can include code blocks with syntax highlighting:

```python
def hello_markdeck():
    print("Hello from MarkDeck!")
    return "Awesome presentations"
```

---

## Speaker Notes

You can add speaker notes that only appear in the terminal where you run markdeck.

<!--NOTES:
These are speaker notes.
They will appear in the terminal when you navigate to this slide.
The audience won't see them in the browser presentation.
-->

---

## Keyboard Shortcuts

Press `?` to see all available shortcuts

| Key | Action |
|-----|--------|
| → / Space | Next slide |
| ← | Previous slide |
| F | Fullscreen |

---

## Thank You!

Start creating your presentation now:

```bash
markdeck present {filename.name}
```

Visit the documentation for more features!
"""

    filename.write_text(template, encoding='utf-8')
    click.echo(f"Created presentation: {filename}")
    click.echo("\nStart presenting with:")
    click.echo(f"  markdeck present {filename}")


@main.command()
@click.argument('file', type=click.Path(exists=True, path_type=Path))
def validate(file: Path):
    """
    Validate a markdown presentation file.

    Example: markdeck validate my-slides.md
    """
    from markdeck.parser import SlideParser

    try:
        parser = SlideParser(file)
        slides = parser.parse()
        title = parser.get_title()

        click.echo("✓ File is valid")
        click.echo(f"  Title: {title}")
        click.echo(f"  Slides: {len(slides)}")

        # Check for potential issues
        warnings = []
        for i, slide in enumerate(slides, 1):
            if not slide.content.strip():
                warnings.append(f"  - Slide {i}: Empty content")
            if len(slide.content) > 2000:
                warnings.append(f"  - Slide {i}: Very long content ({len(slide.content)} chars)")

        if warnings:
            click.echo("\nWarnings:")
            for warning in warnings:
                click.echo(warning)

    except FileNotFoundError:
        click.echo(f"✗ File not found: {file}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"✗ Error validating file: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
