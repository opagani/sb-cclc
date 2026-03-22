import os
import sys
from datetime import datetime
from pathlib import Path

import click
from loguru import logger

FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level.name:.3}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)


def configure_logging():
    """Configure loguru for console and file logging.

    Removes the default handler and sets up:
    - stderr handler at LOG_LEVEL (default: INFO, configurable via env var)
    - File handler at DEBUG level writing to LOG_FILE (default: app.log)

    Log format: ``YYYY-MM-DD HH:mm:ss | LVL | module:func:line | message``
    where LVL is a 3-char abbreviation (INF, DBG, WRN, ERR, CRT).
    """
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    log_file = os.environ.get("LOG_FILE", "app.log")
    logger.remove()
    logger.add(sys.stderr, level=log_level, format=FORMAT)
    logger.add(log_file, level="DEBUG", rotation="50 KB", retention=1, format=FORMAT)


def get_notes_dir():
    """Return the notes storage directory from NOTES_DIR env var.

    Defaults to ``~/second_brain`` when the variable is unset.
    """
    return Path(os.environ.get("NOTES_DIR", Path.home() / "second_brain"))


@click.group()
def cli():
    """Second Brain — capture and recall quick thoughts."""
    configure_logging()


@cli.command()
@click.argument("thought")
def new(thought):
    """Save a new thought as a markdown file."""
    notes_dir = get_notes_dir()
    notes_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filepath = notes_dir / f"{timestamp}.md"
    filepath.write_text(thought + "\n")

    logger.info("Saved note: {}", filepath.name)
    click.echo(f"Saved: {filepath}")


def _get_sorted_notes():
    """Return sorted list of markdown files in the notes directory."""
    notes_dir = get_notes_dir()
    if not notes_dir.exists():
        return []
    return sorted(f for f in notes_dir.iterdir() if f.suffix == ".md")


@cli.command("list")
def list_notes():
    """List all saved notes."""
    notes_dir = get_notes_dir()
    click.echo(f"Notes in: {notes_dir}")

    files = _get_sorted_notes()
    if not files:
        click.echo("No notes yet.")
        return

    for i, f in enumerate(files, 1):
        click.echo(f"{i}. {f.name}")


@cli.command()
@click.argument("number", type=int)
def show(number):
    """Print the content of a note by its list number."""
    files = _get_sorted_notes()
    if not files or number < 1 or number > len(files):
        raise click.ClickException(f"Invalid note number: {number}")
    click.echo(files[number - 1].read_text(), nl=False)


def main():
    """Entry point for the CLI."""
    cli()
