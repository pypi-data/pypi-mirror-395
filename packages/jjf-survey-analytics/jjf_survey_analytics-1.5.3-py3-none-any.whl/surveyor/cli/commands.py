"""
CLI commands for the Surveyor application.
"""

import logging
import sys

import click
from sqlalchemy.orm import sessionmaker

from ..config.container import container
from ..config.settings import AppConfig
from ..models.base import create_database_engine, create_session_factory, create_tables
from ..repositories.spreadsheet_repository import (
    DataExtractionJobRepository,
    SheetCellRepository,
    SheetColumnRepository,
    SheetRepository,
    SheetRowRepository,
    SpreadsheetRepository,
)
from ..services.data_extraction_service import DataExtractionService
from ..services.google_sheets_service import GoogleSheetsService, MockGoogleSheetsService

logger = logging.getLogger(__name__)


def setup_dependencies(config: AppConfig):
    """Set up dependency injection container."""
    # Create database engine and session factory
    engine = create_database_engine(config.database.url, config.database.echo)
    session_factory = create_session_factory(engine)

    # Register session factory
    container.register_instance(sessionmaker, session_factory)

    # Register configuration
    container.register_instance(AppConfig, config)

    # Register Google Sheets service
    try:
        sheets_service = GoogleSheetsService(config.google_sheets)
        container.register_instance(GoogleSheetsService, sheets_service)
    except ImportError:
        logger.warning("Google API libraries not available, using mock service")
        sheets_service = MockGoogleSheetsService()
        container.register_instance(GoogleSheetsService, sheets_service)

    return engine, session_factory


@click.command()
@click.pass_context
def init_db(ctx):
    """Initialize the database schema."""
    config = ctx.obj["config"]

    try:
        engine, _ = setup_dependencies(config)

        click.echo("Creating database tables...")
        create_tables(engine)
        click.echo("✅ Database initialized successfully!")

    except Exception as e:
        click.echo(f"❌ Error initializing database: {e}")
        if ctx.obj["verbose"]:
            logger.exception("Database initialization failed")
        sys.exit(1)


@click.command()
@click.option(
    "--urls", "-u", multiple=True, help="Specific URLs to extract (can be used multiple times)"
)
@click.option("--job-name", "-n", help="Name for the extraction job")
@click.option("--use-default-urls", "-d", is_flag=True, help="Use default configured URLs")
@click.pass_context
def extract(ctx, urls, job_name, use_default_urls):
    """Extract data from Google Sheets."""
    config = ctx.obj["config"]

    # Determine which URLs to process
    urls_to_process = []

    if urls:
        urls_to_process.extend(urls)

    if use_default_urls or not urls:
        urls_to_process.extend(config.sheet_urls)

    if not urls_to_process:
        click.echo("❌ No URLs specified. Use --urls or --use-default-urls")
        return

    try:
        # Set up dependencies
        engine, session_factory = setup_dependencies(config)

        # Create session
        session = session_factory()

        try:
            # Create repositories
            spreadsheet_repo = SpreadsheetRepository(session)
            sheet_repo = SheetRepository(session)
            column_repo = SheetColumnRepository(session)
            row_repo = SheetRowRepository(session)
            cell_repo = SheetCellRepository(session)
            job_repo = DataExtractionJobRepository(session)

            # Get sheets service
            sheets_service = container.get(GoogleSheetsService)

            # Create extraction service
            extraction_service = DataExtractionService(
                sheets_service=sheets_service,
                spreadsheet_repo=spreadsheet_repo,
                sheet_repo=sheet_repo,
                column_repo=column_repo,
                row_repo=row_repo,
                cell_repo=cell_repo,
                job_repo=job_repo,
            )

            click.echo(f"🚀 Starting extraction of {len(urls_to_process)} spreadsheet(s)...")

            # Start extraction
            job = extraction_service.extract_and_normalize(urls_to_process, job_name)

            if job.status == "completed":
                click.echo("✅ Extraction completed successfully!")
                click.echo(f"   Job ID: {job.id}")
                click.echo(f"   Processed {job.processed_sheets} sheets")
                click.echo(f"   Processed {job.processed_rows} rows")
            else:
                click.echo(f"❌ Extraction failed: {job.error_message}")

        finally:
            session.close()

    except Exception as e:
        click.echo(f"❌ Error during extraction: {e}")
        if ctx.obj["verbose"]:
            logger.exception("Extraction failed")
        sys.exit(1)


@click.command()
@click.option("--limit", "-l", default=10, help="Number of recent jobs to show")
@click.pass_context
def status(ctx, limit):
    """Show status of recent extraction jobs."""
    config = ctx.obj["config"]

    try:
        # Set up dependencies
        engine, session_factory = setup_dependencies(config)

        # Create session
        session = session_factory()

        try:
            # Create job repository
            job_repo = DataExtractionJobRepository(session)

            # Get recent jobs
            jobs = job_repo.get_latest_jobs(limit)

            if not jobs:
                click.echo("No extraction jobs found.")
                return

            click.echo(f"Recent extraction jobs (last {len(jobs)}):")
            click.echo()

            for job in jobs:
                status_icon = {
                    "completed": "✅",
                    "running": "🔄",
                    "failed": "❌",
                    "pending": "⏳",
                }.get(job.status, "❓")

                click.echo(f"{status_icon} Job {job.id}: {job.job_name}")
                click.echo(f"   Status: {job.status}")
                click.echo(f"   Created: {job.created_at}")
                if job.completed_at:
                    click.echo(f"   Completed: {job.completed_at}")
                click.echo(
                    f"   Progress: {job.processed_sheets}/{job.total_sheets} sheets, "
                    f"{job.processed_rows}/{job.total_rows} rows"
                )
                if job.error_message:
                    click.echo(f"   Error: {job.error_message}")
                click.echo()

        finally:
            session.close()

    except Exception as e:
        click.echo(f"❌ Error getting status: {e}")
        if ctx.obj["verbose"]:
            logger.exception("Status check failed")
        sys.exit(1)
