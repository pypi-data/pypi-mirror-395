"""
Main CLI interface for the Surveyor application.
"""

import logging

import click

from ..config.settings import load_config
from .commands import extract, init_db, status


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.option("--config-file", "-c", type=click.Path(exists=True), help="Configuration file path")
@click.pass_context
def cli(ctx, verbose, config_file):
    """
    Surveyor - Extract and normalize data from Google Sheets.

    A tool for extracting data from Google Spreadsheets and storing it
    in a normalized SQLite database using Service-Oriented Architecture.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)

    # Set up logging
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Load configuration
    config = load_config()
    ctx.obj["config"] = config

    # Store verbose flag
    ctx.obj["verbose"] = verbose


# Add command groups
cli.add_command(extract)
cli.add_command(status)
cli.add_command(init_db)


@cli.command()
@click.pass_context
def version(ctx):
    """Show version information."""
    from .. import __version__

    click.echo(f"Surveyor version {__version__}")


@cli.command()
@click.pass_context
def config_info(ctx):
    """Show current configuration."""
    config = ctx.obj["config"]

    click.echo("Current Configuration:")
    click.echo(f"  Database URL: {config.database.url}")
    click.echo(f"  Log Level: {config.logging.level}")
    click.echo(f"  Google Credentials: {config.google_sheets.credentials_file or 'Not configured'}")
    click.echo(f"  Number of sheet URLs: {len(config.sheet_urls)}")


if __name__ == "__main__":
    cli()
