#!/usr/bin/env python3
"""
Schema Manager - Database Schema Management

Handles database schema creation, validation, and management for survey data.
Supports both SQLite (development) and PostgreSQL (production) databases.

Extracted from SurveyNormalizer as part of God class decomposition.
"""

import logging
import os

# Import db_utils from scripts (existing location)
import sys
import threading
from contextlib import contextmanager
from typing import Any, Dict, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../scripts/utils"))
from db_utils import DatabaseConnection, adapt_sql_for_postgresql, is_postgresql

logger = logging.getLogger(__name__)


class SchemaManager:
    """
    Manages database schema for survey data.

    Responsibilities:
    - Define and create database tables
    - Create indexes for performance
    - Validate schema integrity
    - Handle schema migrations
    - Thread-safe operations
    """

    def __init__(self, db_path: str):
        """
        Initialize schema manager.

        Args:
            db_path: Path to database (SQLite file path or ignored for PostgreSQL)
        """
        self.db_path = db_path
        self.db_connection = DatabaseConnection(db_path)
        self.use_postgresql = is_postgresql()
        self._lock = threading.Lock()

        logger.info(
            f"SchemaManager initialized for {'PostgreSQL' if self.use_postgresql else f'SQLite ({db_path})'}"
        )

    @contextmanager
    def _get_connection(self):
        """Get database connection with automatic cleanup."""
        conn = self.db_connection.get_connection()
        try:
            yield conn
        finally:
            conn.close()

    def create_schema(self) -> None:
        """
        Create all database tables and indexes.

        Creates the full normalized database schema including:
        - surveys: Survey metadata
        - survey_questions: Question definitions
        - respondents: Unique respondent tracking
        - survey_responses: Response records
        - survey_answers: Individual answer data
        - normalization_jobs: Normalization job tracking
        - sync_tracking: Data synchronization tracking

        Thread-safe operation.
        """
        with self._lock:
            logger.info("Creating database schema...")

            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Drop existing tables (reverse order due to foreign keys)
                self._drop_tables(cursor)

                # Create tables in dependency order
                self._create_surveys_table(cursor)
                self._create_survey_questions_table(cursor)
                self._create_respondents_table(cursor)
                self._create_survey_responses_table(cursor)
                self._create_survey_answers_table(cursor)
                self._create_normalization_jobs_table(cursor)
                self._create_sync_tracking_table(cursor)

                # Create indexes for performance
                self.create_indexes(cursor)

                conn.commit()

            db_type = "PostgreSQL" if self.use_postgresql else f"SQLite ({self.db_path})"
            logger.info(f"Schema created successfully: {db_type}")

    def _drop_tables(self, cursor) -> None:
        """Drop all tables in reverse dependency order."""
        tables_to_drop = [
            "survey_answers",
            "survey_responses",
            "survey_questions",
            "surveys",
            "respondents",
            "normalization_jobs",
            "sync_tracking",
        ]

        for table in tables_to_drop:
            if self.use_postgresql:
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
            else:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")

        logger.debug(f"Dropped {len(tables_to_drop)} tables")

    def _create_surveys_table(self, cursor) -> None:
        """Create surveys table."""
        cursor.execute(
            adapt_sql_for_postgresql(
                """
            CREATE TABLE surveys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                survey_name TEXT NOT NULL,
                survey_type TEXT NOT NULL,
                spreadsheet_id TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(spreadsheet_id)
            )
        """
            )
        )
        logger.debug("Created surveys table")

    def _create_survey_questions_table(self, cursor) -> None:
        """Create survey_questions table."""
        cursor.execute(
            adapt_sql_for_postgresql(
                """
            CREATE TABLE survey_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                survey_id INTEGER NOT NULL,
                question_key TEXT NOT NULL,
                question_text TEXT,
                question_type TEXT DEFAULT 'text',
                question_order INTEGER,
                is_required BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (survey_id) REFERENCES surveys (id),
                UNIQUE(survey_id, question_key)
            )
        """
            )
        )
        logger.debug("Created survey_questions table")

    def _create_respondents_table(self, cursor) -> None:
        """Create respondents table."""
        cursor.execute(
            adapt_sql_for_postgresql(
                """
            CREATE TABLE respondents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                respondent_hash TEXT UNIQUE NOT NULL,
                browser TEXT,
                device TEXT,
                ip_address TEXT,
                user_agent TEXT,
                first_response_date TIMESTAMP,
                last_response_date TIMESTAMP,
                total_responses INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
            )
        )
        logger.debug("Created respondents table")

    def _create_survey_responses_table(self, cursor) -> None:
        """Create survey_responses table."""
        cursor.execute(
            adapt_sql_for_postgresql(
                """
            CREATE TABLE survey_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                survey_id INTEGER NOT NULL,
                respondent_id INTEGER NOT NULL,
                response_date TIMESTAMP NOT NULL,
                completion_status TEXT DEFAULT 'complete',
                response_duration_seconds INTEGER,
                source_row_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (survey_id) REFERENCES surveys (id),
                FOREIGN KEY (respondent_id) REFERENCES respondents (id)
            )
        """
            )
        )
        logger.debug("Created survey_responses table")

    def _create_survey_answers_table(self, cursor) -> None:
        """Create survey_answers table."""
        cursor.execute(
            adapt_sql_for_postgresql(
                """
            CREATE TABLE survey_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                response_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                answer_text TEXT,
                answer_numeric REAL,
                answer_boolean BOOLEAN,
                answer_date TIMESTAMP,
                is_empty BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (response_id) REFERENCES survey_responses (id),
                FOREIGN KEY (question_id) REFERENCES survey_questions (id),
                UNIQUE(response_id, question_id)
            )
        """
            )
        )
        logger.debug("Created survey_answers table")

    def _create_normalization_jobs_table(self, cursor) -> None:
        """Create normalization_jobs table."""
        cursor.execute(
            adapt_sql_for_postgresql(
                """
            CREATE TABLE normalization_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_name TEXT NOT NULL,
                status TEXT DEFAULT 'running',
                surveys_processed INTEGER DEFAULT 0,
                responses_processed INTEGER DEFAULT 0,
                questions_created INTEGER DEFAULT 0,
                answers_created INTEGER DEFAULT 0,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                error_message TEXT
            )
        """
            )
        )
        logger.debug("Created normalization_jobs table")

    def _create_sync_tracking_table(self, cursor) -> None:
        """Create sync_tracking table."""
        cursor.execute(
            adapt_sql_for_postgresql(
                """
            CREATE TABLE sync_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                spreadsheet_id TEXT UNIQUE NOT NULL,
                last_sync_timestamp TIMESTAMP,
                last_source_update TIMESTAMP,
                row_count INTEGER DEFAULT 0,
                sync_status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
            )
        )
        logger.debug("Created sync_tracking table")

    def create_indexes(self, cursor=None) -> None:
        """
        Create all database indexes for performance.

        Creates indexes on:
        - Foreign key columns for JOIN performance
        - Frequently queried columns
        - Unique constraint columns

        Args:
            cursor: Database cursor (optional, creates new connection if None)
        """
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_survey_questions_survey ON survey_questions(survey_id)",
            "CREATE INDEX IF NOT EXISTS idx_survey_responses_survey ON survey_responses(survey_id)",
            "CREATE INDEX IF NOT EXISTS idx_survey_responses_respondent ON survey_responses(respondent_id)",
            "CREATE INDEX IF NOT EXISTS idx_survey_responses_date ON survey_responses(response_date)",
            "CREATE INDEX IF NOT EXISTS idx_survey_answers_response ON survey_answers(response_id)",
            "CREATE INDEX IF NOT EXISTS idx_survey_answers_question ON survey_answers(question_id)",
            "CREATE INDEX IF NOT EXISTS idx_respondents_hash ON respondents(respondent_hash)",
            "CREATE INDEX IF NOT EXISTS idx_respondents_first_response ON respondents(first_response_date)",
        ]

        if cursor is None:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                for index_sql in indexes:
                    cursor.execute(index_sql)
                conn.commit()
        else:
            for index_sql in indexes:
                cursor.execute(index_sql)

        logger.debug(f"Created {len(indexes)} indexes")

    def validate_schema(self) -> bool:
        """
        Validate that all required tables and columns exist.

        Returns:
            True if schema is valid, False otherwise
        """
        required_tables = [
            "surveys",
            "survey_questions",
            "respondents",
            "survey_responses",
            "survey_answers",
            "normalization_jobs",
            "sync_tracking",
        ]

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                for table in required_tables:
                    # Check if table exists
                    if self.use_postgresql:
                        cursor.execute(
                            """
                            SELECT EXISTS (
                                SELECT FROM information_schema.tables
                                WHERE table_name = %s
                            )
                        """,
                            (table,),
                        )
                    else:
                        cursor.execute(
                            """
                            SELECT name FROM sqlite_master
                            WHERE type='table' AND name=?
                        """,
                            (table,),
                        )

                    result = cursor.fetchone()

                    # Handle different result formats
                    if self.use_postgresql:
                        exists = result["exists"] if isinstance(result, dict) else result[0]
                    else:
                        exists = result is not None

                    if not exists:
                        logger.error(f"Table '{table}' does not exist")
                        return False

            logger.info("Schema validation successful")
            return True

        except Exception as e:
            logger.error(f"Schema validation failed: {e}")
            return False

    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """
        Get schema definition for a specific table.

        Args:
            table_name: Name of the table

        Returns:
            Dictionary with table schema information including columns and types
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                if self.use_postgresql:
                    cursor.execute(
                        """
                        SELECT column_name, data_type, is_nullable, column_default
                        FROM information_schema.columns
                        WHERE table_name = %s
                        ORDER BY ordinal_position
                    """,
                        (table_name,),
                    )
                else:
                    cursor.execute(f"PRAGMA table_info({table_name})")

                columns = cursor.fetchall()

                if not columns:
                    logger.warning(f"Table '{table_name}' not found")
                    return {}

                # Format results
                if self.use_postgresql:
                    schema = {
                        "table_name": table_name,
                        "columns": [
                            {
                                "name": col["column_name"] if isinstance(col, dict) else col[0],
                                "type": col["data_type"] if isinstance(col, dict) else col[1],
                                "nullable": col["is_nullable"] if isinstance(col, dict) else col[2],
                                "default": (
                                    col["column_default"] if isinstance(col, dict) else col[3]
                                ),
                            }
                            for col in columns
                        ],
                    }
                else:
                    schema = {
                        "table_name": table_name,
                        "columns": [
                            {
                                "name": col["name"] if isinstance(col, dict) else col[1],
                                "type": col["type"] if isinstance(col, dict) else col[2],
                                "nullable": not (
                                    col["notnull"] if isinstance(col, dict) else col[3]
                                ),
                                "default": col["dflt_value"] if isinstance(col, dict) else col[4],
                                "primary_key": bool(col["pk"] if isinstance(col, dict) else col[5]),
                            }
                            for col in columns
                        ],
                    }

                return schema

        except Exception as e:
            logger.error(f"Failed to get schema for table '{table_name}': {e}")
            return {}

    def drop_schema(self) -> None:
        """
        Drop all tables (for testing/rebuilding).

        Thread-safe operation.
        WARNING: This will delete all data!
        """
        with self._lock:
            logger.warning("Dropping all schema tables...")

            with self._get_connection() as conn:
                cursor = conn.cursor()
                self._drop_tables(cursor)
                conn.commit()

            logger.info("All tables dropped successfully")

    def get_table_names(self) -> List[str]:
        """
        Get list of all table names in the database.

        Returns:
            List of table names
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                if self.use_postgresql:
                    cursor.execute(
                        """
                        SELECT table_name
                        FROM information_schema.tables
                        WHERE table_schema = 'public'
                        ORDER BY table_name
                    """
                    )
                else:
                    cursor.execute(
                        """
                        SELECT name FROM sqlite_master
                        WHERE type='table'
                        ORDER BY name
                    """
                    )

                tables = cursor.fetchall()
                return [t["table_name"] if isinstance(t, dict) else t[0] for t in tables]

        except Exception as e:
            logger.error(f"Failed to get table names: {e}")
            return []


def get_schema_manager(db_path: str = "survey_normalized.db") -> SchemaManager:
    """
    Factory function to get SchemaManager instance.

    Args:
        db_path: Path to database file (SQLite only, ignored for PostgreSQL)

    Returns:
        SchemaManager instance
    """
    return SchemaManager(db_path)
