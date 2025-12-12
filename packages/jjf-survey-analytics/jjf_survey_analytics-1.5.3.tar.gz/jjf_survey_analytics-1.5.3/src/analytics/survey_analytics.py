#!/usr/bin/env python3
"""
Survey Analytics Module

Provides statistical analysis and reporting capabilities for the normalized survey database.
"""

import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional


class SurveyAnalytics:
    """Analytics engine for survey data."""

    def __init__(
        self,
        db_path: str = "survey_normalized.db",
        use_postgresql: bool = None,
        database_url: str = None,
    ):
        """Initialize SurveyAnalytics with optional PostgreSQL support.

        Args:
            db_path: Path to SQLite database file (used if not PostgreSQL)
            use_postgresql: Override PostgreSQL detection (defaults to checking DATABASE_URL env var)
            database_url: PostgreSQL connection string (defaults to DATABASE_URL env var)
        """
        self.db_path = db_path

        # Auto-detect PostgreSQL mode from environment if not specified
        if use_postgresql is None:
            use_postgresql = os.getenv("DATABASE_URL") is not None

        self.use_postgresql = use_postgresql
        self.database_url = database_url or os.getenv("DATABASE_URL")

    def get_connection(self):
        """Get database connection with row factory."""
        if self.use_postgresql:
            import psycopg2
            import psycopg2.extras

            conn = psycopg2.connect(self.database_url)
            conn.cursor_factory = psycopg2.extras.RealDictCursor
            return conn
        else:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn

    def get_survey_overview(self) -> Dict[str, Any]:
        """Get high-level survey statistics."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Basic counts
            cursor.execute("SELECT COUNT(*) as count FROM surveys")
            total_surveys = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM survey_responses")
            total_responses = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(DISTINCT respondent_id) as count FROM survey_responses")
            unique_respondents = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM survey_questions")
            total_questions = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM survey_answers WHERE is_empty = false")
            answered_questions = cursor.fetchone()["count"]

            # Response rate calculation
            total_possible_answers = total_responses * total_questions if total_questions > 0 else 0
            response_rate = (
                (answered_questions / total_possible_answers * 100)
                if total_possible_answers > 0
                else 0
            )

            # Recent activity - database-agnostic date handling
            if self.use_postgresql:
                cursor.execute(
                    """
                    SELECT COUNT(*) as count
                    FROM survey_responses
                    WHERE created_at >= NOW() - INTERVAL '7 days'
                """
                )
            else:
                cursor.execute(
                    """
                    SELECT COUNT(*) as count
                    FROM survey_responses
                    WHERE created_at >= datetime('now', '-7 days')
                """
                )
            recent_responses = cursor.fetchone()["count"]

            return {
                "total_surveys": total_surveys,
                "total_responses": total_responses,
                "unique_respondents": unique_respondents,
                "total_questions": total_questions,
                "answered_questions": answered_questions,
                "response_rate": round(response_rate, 1),
                "recent_responses": recent_responses,
            }

    def get_survey_breakdown(self) -> List[Dict[str, Any]]:
        """Get breakdown by survey type."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    s.id,
                    s.survey_name,
                    s.survey_type,
                    COUNT(DISTINCT sr.id) as response_count,
                    COUNT(DISTINCT sr.respondent_id) as unique_respondents,
                    COUNT(DISTINCT sq.id) as question_count,
                    AVG(CASE WHEN sa.is_empty = false THEN 1.0 ELSE 0.0 END) as completion_rate,
                    MIN(sr.created_at) as first_response,
                    MAX(sr.created_at) as last_response
                FROM surveys s
                LEFT JOIN survey_responses sr ON s.id = sr.survey_id
                LEFT JOIN survey_questions sq ON s.id = sq.survey_id
                LEFT JOIN survey_answers sa ON sr.id = sa.response_id
                GROUP BY s.id, s.survey_name, s.survey_type
                ORDER BY response_count DESC
            """
            )

            return [dict(row) for row in cursor.fetchall()]

    def get_response_activity(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get response activity over time."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Database-agnostic date filtering
            if self.use_postgresql:
                query = """
                    SELECT
                        DATE(sr.created_at) as response_date,
                        COUNT(*) as response_count,
                        COUNT(DISTINCT sr.respondent_id) as unique_respondents,
                        s.survey_type,
                        s.survey_name
                    FROM survey_responses sr
                    JOIN surveys s ON sr.survey_id = s.id
                    WHERE sr.created_at >= NOW() - INTERVAL '{days} days'
                    GROUP BY DATE(sr.created_at), s.survey_type, s.survey_name
                    ORDER BY response_date DESC
                """
            else:
                query = """
                    SELECT
                        DATE(sr.created_at) as response_date,
                        COUNT(*) as response_count,
                        COUNT(DISTINCT sr.respondent_id) as unique_respondents,
                        s.survey_type,
                        s.survey_name
                    FROM survey_responses sr
                    JOIN surveys s ON sr.survey_id = s.id
                    WHERE sr.created_at >= datetime('now', '-{days} days')
                    GROUP BY DATE(sr.created_at), s.survey_type, s.survey_name
                    ORDER BY response_date DESC
                """

            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    def get_respondent_analysis(self) -> Dict[str, Any]:
        """Analyze respondent patterns."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Browser breakdown
            cursor.execute(
                """
                SELECT 
                    browser,
                    COUNT(*) as count,
                    COUNT(DISTINCT respondent_hash) as unique_users
                FROM respondents
                WHERE browser IS NOT NULL AND browser != ''
                GROUP BY browser
                ORDER BY count DESC
            """
            )
            browser_stats = [dict(row) for row in cursor.fetchall()]

            # Device breakdown
            cursor.execute(
                """
                SELECT 
                    device,
                    COUNT(*) as count,
                    COUNT(DISTINCT respondent_hash) as unique_users
                FROM respondents
                WHERE device IS NOT NULL AND device != ''
                GROUP BY device
                ORDER BY count DESC
            """
            )
            device_stats = [dict(row) for row in cursor.fetchall()]

            # Response frequency
            cursor.execute(
                """
                SELECT 
                    total_responses,
                    COUNT(*) as respondent_count
                FROM respondents
                GROUP BY total_responses
                ORDER BY total_responses
            """
            )
            frequency_stats = [dict(row) for row in cursor.fetchall()]

            return {
                "browser_breakdown": browser_stats,
                "device_breakdown": device_stats,
                "response_frequency": frequency_stats,
            }

    def get_question_analytics(self, survey_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get analytics for survey questions."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Use different parameter placeholder for PostgreSQL vs SQLite
            param_placeholder = "%s" if self.use_postgresql else "?"
            where_clause = f"WHERE sq.survey_id = {param_placeholder}" if survey_id else ""
            params = [survey_id] if survey_id else []

            cursor.execute(
                """
                SELECT
                    sq.id,
                    sq.question_key,
                    sq.question_text,
                    s.survey_name,
                    COUNT(sa.id) as total_answers,
                    COUNT(CASE WHEN sa.is_empty = false THEN 1 END) as answered_count,
                    COUNT(CASE WHEN sa.is_empty = true THEN 1 END) as empty_count,
                    ROUND(AVG(CASE WHEN sa.is_empty = false THEN 1.0 ELSE 0.0 END) * 100, 1) as response_rate,
                    COUNT(DISTINCT sa.answer_text) as unique_answers,
                    AVG(sa.answer_numeric) as avg_numeric_value,
                    COUNT(CASE WHEN sa.answer_boolean = true THEN 1 END) as true_count,
                    COUNT(CASE WHEN sa.answer_boolean = false THEN 1 END) as false_count
                FROM survey_questions sq
                JOIN surveys s ON sq.survey_id = s.id
                LEFT JOIN survey_answers sa ON sq.id = sa.question_id
                {where_clause}
                GROUP BY sq.id, sq.question_key, sq.question_text, s.survey_name
                ORDER BY response_rate DESC, answered_count DESC
            """,
                params,
            )

            return [dict(row) for row in cursor.fetchall()]

    def get_answer_distribution(self, question_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get answer distribution for a specific question."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Use different parameter placeholder for PostgreSQL vs SQLite
            param_placeholder = "%s" if self.use_postgresql else "?"

            cursor.execute(
                """
                SELECT
                    answer_text,
                    COUNT(*) as count,
                    ROUND(COUNT(*) * 100.0 / (
                        SELECT COUNT(*)
                        FROM survey_answers
                        WHERE question_id = {param_placeholder} AND is_empty = false
                    ), 1) as percentage
                FROM survey_answers
                WHERE question_id = {param_placeholder} AND is_empty = false
                GROUP BY answer_text
                ORDER BY count DESC
                LIMIT {param_placeholder}
            """,
                (question_id, question_id, limit),
            )

            return [dict(row) for row in cursor.fetchall()]

    def get_survey_completion_stats(self) -> List[Dict[str, Any]]:
        """Get completion statistics by survey."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    s.id,
                    s.survey_name,
                    s.survey_type,
                    COUNT(DISTINCT sr.id) as total_responses,
                    COUNT(DISTINCT sq.id) as total_questions,
                    COUNT(sa.id) as total_possible_answers,
                    COUNT(CASE WHEN sa.is_empty = false THEN 1 END) as actual_answers,
                    ROUND(
                        COUNT(CASE WHEN sa.is_empty = false THEN 1 END) * 100.0 /
                        NULLIF(COUNT(sa.id), 0), 1
                    ) as completion_percentage,
                    AVG(
                        CASE WHEN sa.is_empty = false THEN 1.0 ELSE 0.0 END
                    ) as avg_question_completion
                FROM surveys s
                LEFT JOIN survey_responses sr ON s.id = sr.survey_id
                LEFT JOIN survey_questions sq ON s.id = sq.survey_id
                LEFT JOIN survey_answers sa ON sr.id = sa.response_id AND sq.id = sa.question_id
                GROUP BY s.id, s.survey_name, s.survey_type
                ORDER BY completion_percentage DESC
            """
            )

            return [dict(row) for row in cursor.fetchall()]

    def get_time_series_data(self, days: int = 30) -> Dict[str, Any]:
        """Get time series data for charts."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Database-agnostic date filtering for daily response counts
            if self.use_postgresql:
                daily_query = """
                    SELECT
                        DATE(created_at) as date,
                        COUNT(*) as responses,
                        COUNT(DISTINCT respondent_id) as unique_respondents
                    FROM survey_responses
                    WHERE created_at >= NOW() - INTERVAL '{days} days'
                    GROUP BY DATE(created_at)
                    ORDER BY date
                """
            else:
                daily_query = """
                    SELECT
                        DATE(created_at) as date,
                        COUNT(*) as responses,
                        COUNT(DISTINCT respondent_id) as unique_respondents
                    FROM survey_responses
                    WHERE created_at >= datetime('now', '-{days} days')
                    GROUP BY DATE(created_at)
                    ORDER BY date
                """

            cursor.execute(daily_query)
            daily_data = [dict(row) for row in cursor.fetchall()]

            # Database-agnostic date filtering for survey type breakdown
            if self.use_postgresql:
                breakdown_query = """
                    SELECT
                        DATE(sr.created_at) as date,
                        s.survey_type,
                        COUNT(*) as responses
                    FROM survey_responses sr
                    JOIN surveys s ON sr.survey_id = s.id
                    WHERE sr.created_at >= NOW() - INTERVAL '{days} days'
                    GROUP BY DATE(sr.created_at), s.survey_type
                    ORDER BY date, s.survey_type
                """
            else:
                breakdown_query = """
                    SELECT
                        DATE(sr.created_at) as date,
                        s.survey_type,
                        COUNT(*) as responses
                    FROM survey_responses sr
                    JOIN surveys s ON sr.survey_id = s.id
                    WHERE sr.created_at >= datetime('now', '-{days} days')
                    GROUP BY DATE(sr.created_at), s.survey_type
                    ORDER BY date, s.survey_type
                """

            cursor.execute(breakdown_query)
            type_breakdown = [dict(row) for row in cursor.fetchall()]

            return {"daily_responses": daily_data, "type_breakdown": type_breakdown}

    def search_responses(
        self, search_term: str, survey_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Search through survey responses."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Use different parameter placeholder for PostgreSQL vs SQLite
            param_placeholder = "%s" if self.use_postgresql else "?"

            where_clauses = [f"sa.answer_text LIKE {param_placeholder}"]
            params = [f"%{search_term}%"]

            if survey_id:
                where_clauses.append(f"s.id = {param_placeholder}")
                params.append(survey_id)

            where_clause = " AND ".join(where_clauses)

            cursor.execute(
                """
                SELECT
                    s.survey_name,
                    sq.question_key,
                    sq.question_text,
                    sa.answer_text,
                    sr.created_at as response_date,
                    r.browser,
                    r.device
                FROM survey_answers sa
                JOIN survey_questions sq ON sa.question_id = sq.id
                JOIN survey_responses sr ON sa.response_id = sr.id
                JOIN surveys s ON sr.survey_id = s.id
                JOIN respondents r ON sr.respondent_id = r.id
                WHERE {where_clause}
                ORDER BY sr.created_at DESC
                LIMIT 100
            """,
                params,
            )

            return [dict(row) for row in cursor.fetchall()]

    def export_survey_data(self, survey_id: int) -> Dict[str, Any]:
        """Export complete survey data for analysis."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Use different parameter placeholder for PostgreSQL vs SQLite
            param_placeholder = "%s" if self.use_postgresql else "?"

            # Get survey info
            cursor.execute(f"SELECT * FROM surveys WHERE id = {param_placeholder}", (survey_id,))
            survey_info = dict(cursor.fetchone())

            # Get all responses with answers
            cursor.execute(
                """
                SELECT
                    sr.id as response_id,
                    sr.created_at as response_date,
                    r.browser,
                    r.device,
                    r.respondent_hash,
                    sq.question_key,
                    sq.question_text,
                    sa.answer_text,
                    sa.answer_numeric,
                    sa.answer_boolean,
                    sa.is_empty
                FROM survey_responses sr
                JOIN respondents r ON sr.respondent_id = r.id
                JOIN survey_answers sa ON sr.id = sa.response_id
                JOIN survey_questions sq ON sa.question_id = sq.id
                WHERE sr.survey_id = {param_placeholder}
                ORDER BY sr.created_at, sq.question_order
            """,
                (survey_id,),
            )

            responses = [dict(row) for row in cursor.fetchall()]

            return {
                "survey_info": survey_info,
                "responses": responses,
                "export_date": datetime.now().isoformat(),
            }
