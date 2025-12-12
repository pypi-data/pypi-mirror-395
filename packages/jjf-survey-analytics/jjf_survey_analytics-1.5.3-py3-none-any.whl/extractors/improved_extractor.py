#!/usr/bin/env python3
"""
Improved Google Sheets Data Extractor

Updated version that properly handles all the Google Sheets URLs
and extracts data using multiple methods.

Supports both SQLite (local) and PostgreSQL (production) via DATABASE_URL.
"""

import csv
import json
import logging
import os
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime
from typing import Any, Dict, List

from db_utils import DatabaseConnection, adapt_sql_for_postgresql, get_placeholder, is_postgresql

logger = logging.getLogger(__name__)


class ImprovedExtractor:
    """Improved data extractor for Google Sheets."""

    def __init__(self, db_path: str = "surveyor_data_improved.db"):
        self.db_path = db_path
        self.db_connection = DatabaseConnection(db_path)
        self.use_postgresql = is_postgresql()
        self.placeholder = get_placeholder()

        if self.use_postgresql:
            logger.info("Extractor using PostgreSQL database")
        else:
            logger.info(f"Extractor using SQLite database: {db_path}")

        self.sheet_urls = [
            "https://docs.google.com/spreadsheets/d/1h9AooI-E70v36EOxuErh4uYBg2TLbsF7X5kXdkrUkoQ/edit?usp=sharing",
            "https://docs.google.com/spreadsheets/d/1qEHKDVIO4YTR3TjMt336HdKLIBMV2cebAcvdbGOUdCU/edit?usp=sharing",
            "https://docs.google.com/spreadsheets/d/1fAAXXGOiDWc8lMVaRwqvuM2CDNAyNY_Px3usyisGhaw/edit?usp=sharing",
            "https://docs.google.com/spreadsheets/d/1-aw7gjjvRMQj89lstVBtKDZ67Cs-dO1SHNsp4scJ4II/edit?usp=sharing",
            "https://docs.google.com/spreadsheets/d/1mQxcZ9U1UsVmHstgWdbHuT7bqfVXV4ZNCr9pn0TlVWM/edit?usp=sharing",
            "https://docs.google.com/spreadsheets/d/1f3NKqhNR-CJr_e6_eLSTLbSFuYY8Gm0dxpSL0mlybMA/edit?usp=sharing",
        ]

    def extract_spreadsheet_id(self, url: str) -> str:
        """Extract spreadsheet ID from Google Sheets URL."""
        pattern = r"/spreadsheets/d/([a-zA-Z0-9-_]+)"
        match = re.search(pattern, url)
        if not match:
            raise ValueError(f"Invalid Google Sheets URL: {url}")
        return match.group(1)

    def get_csv_export_url(self, spreadsheet_id: str, gid: str = "0") -> str:
        """Get CSV export URL for a Google Sheet."""
        return (
            f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}"
        )

    def get_public_csv_url(self, spreadsheet_id: str) -> str:
        """Get public CSV URL that works for shared sheets."""
        return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv"

    def download_sheet_data(self, url: str) -> tuple[List[Dict[str, Any]], str]:
        """Download data from a Google Sheet, return data and title."""
        try:
            spreadsheet_id = self.extract_spreadsheet_id(url)

            # Try multiple CSV export methods
            csv_urls = [
                self.get_public_csv_url(spreadsheet_id),
                self.get_csv_export_url(spreadsheet_id, "0"),
                self.get_csv_export_url(spreadsheet_id, "1"),
                self.get_csv_export_url(spreadsheet_id, "2"),
            ]

            print(f"📥 Downloading data from spreadsheet {spreadsheet_id}")

            for i, csv_url in enumerate(csv_urls):
                try:
                    print(f"  Trying method {i+1}: {csv_url}")

                    # Create request with headers
                    req = urllib.request.Request(csv_url)
                    req.add_header(
                        "User-Agent",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    )

                    with urllib.request.urlopen(req, timeout=30) as response:
                        csv_data = response.read().decode("utf-8")

                    # Check if we got actual CSV data
                    if (
                        csv_data.strip()
                        and not csv_data.startswith("<!DOCTYPE")
                        and not csv_data.startswith("<html")
                    ):
                        # Parse CSV
                        lines = csv_data.strip().split("\n")
                        if lines:
                            # Use CSV reader to handle quoted fields properly
                            import io

                            csv_reader = csv.DictReader(io.StringIO(csv_data))
                            data = list(csv_reader)

                            if data:
                                print(
                                    f"✅ Downloaded {len(data)} rows from spreadsheet {spreadsheet_id}"
                                )

                                # Try to extract title from the first method that worked
                                title = self.extract_title_from_url(url, spreadsheet_id)
                                return data, title

                except Exception as e:
                    print(f"    Method {i+1} failed: {e}")
                    continue

            print(f"⚠️  All methods failed for spreadsheet {spreadsheet_id}")
            return [], f"Spreadsheet_{spreadsheet_id}"

        except Exception as e:
            print(f"❌ Error downloading data from {url}: {e}")
            return [], "Error_Spreadsheet"

    def extract_title_from_url(self, url: str, spreadsheet_id: str) -> str:
        """Try to extract the title from the spreadsheet."""
        try:
            # Try to get the title from the edit page
            req = urllib.request.Request(url)
            req.add_header(
                "User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                html_content = response.read().decode("utf-8", errors="ignore")

            # Look for title in the HTML
            title_patterns = [
                r"<title>([^<]+)</title>",
                r'"title":"([^"]+)"',
                r'data-title="([^"]+)"',
            ]

            for pattern in title_patterns:
                match = re.search(pattern, html_content, re.IGNORECASE)
                if match:
                    title = match.group(1).strip()
                    # Clean up the title
                    title = (
                        title.replace(" - Google Sheets", "").replace(" - Google Drive", "").strip()
                    )
                    if title and title != "Google Sheets":
                        return title

        except Exception as e:
            print(f"    Could not extract title: {e}")

        return f"Spreadsheet_{spreadsheet_id}"

    def create_database(self):
        """Create database with improved schema (PostgreSQL or SQLite)."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        # Spreadsheets table
        schema_sql = adapt_sql_for_postgresql(
            """
            CREATE TABLE IF NOT EXISTS spreadsheets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                spreadsheet_id TEXT UNIQUE NOT NULL,
                url TEXT NOT NULL,
                title TEXT,
                sheet_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_synced TIMESTAMP
            )
        """
        )
        cursor.execute(schema_sql)

        # Raw data table
        schema_sql = adapt_sql_for_postgresql(
            """
            CREATE TABLE IF NOT EXISTS raw_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                spreadsheet_id TEXT NOT NULL,
                row_number INTEGER NOT NULL,
                data_json TEXT NOT NULL,
                data_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (spreadsheet_id) REFERENCES spreadsheets (spreadsheet_id)
            )
        """
        )
        cursor.execute(schema_sql)

        # Extraction jobs table
        schema_sql = adapt_sql_for_postgresql(
            """
            CREATE TABLE IF NOT EXISTS extraction_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_name TEXT NOT NULL,
                status TEXT DEFAULT 'running',
                total_spreadsheets INTEGER DEFAULT 0,
                processed_spreadsheets INTEGER DEFAULT 0,
                successful_spreadsheets INTEGER DEFAULT 0,
                total_rows INTEGER DEFAULT 0,
                processed_rows INTEGER DEFAULT 0,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                error_message TEXT
            )
        """
        )
        cursor.execute(schema_sql)

        # Create indexes
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_raw_data_spreadsheet ON raw_data(spreadsheet_id)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_spreadsheets_id ON spreadsheets(spreadsheet_id)"
        )
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_raw_data_hash ON raw_data(data_hash)")

        conn.commit()
        conn.close()

        db_type = "PostgreSQL" if self.use_postgresql else f"SQLite ({self.db_path})"
        print(f"✅ Database created: {db_type}")

    def save_spreadsheet_info(
        self, spreadsheet_id: str, url: str, title: str, sheet_type: str = None
    ):
        """Save spreadsheet information to database."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        # PostgreSQL uses ON CONFLICT, SQLite uses INSERT OR REPLACE
        if self.use_postgresql:
            cursor.execute(
                """
                INSERT INTO spreadsheets (spreadsheet_id, url, title, sheet_type, last_synced)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (spreadsheet_id) DO UPDATE
                SET url = EXCLUDED.url, title = EXCLUDED.title, sheet_type = EXCLUDED.sheet_type, last_synced = EXCLUDED.last_synced
            """,
                (spreadsheet_id, url, title, sheet_type, datetime.now()),
            )
        else:
            cursor.execute(
                """
                INSERT OR REPLACE INTO spreadsheets (spreadsheet_id, url, title, sheet_type, last_synced)
                VALUES (?, ?, ?, ?, ?)
            """,
                (spreadsheet_id, url, title, sheet_type, datetime.now()),
            )

        conn.commit()
        conn.close()

    def save_raw_data(self, spreadsheet_id: str, data: List[Dict[str, Any]]):
        """Save raw data to database with deduplication."""
        if not data:
            return

        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        # Clear existing data for this spreadsheet
        if self.use_postgresql:
            cursor.execute("DELETE FROM raw_data WHERE spreadsheet_id = %s", (spreadsheet_id,))
        else:
            cursor.execute("DELETE FROM raw_data WHERE spreadsheet_id = ?", (spreadsheet_id,))

        # Insert new data with hashing for deduplication
        import hashlib

        for i, row in enumerate(data, 1):
            # Create hash for deduplication
            data_str = json.dumps(row, sort_keys=True)
            data_hash = hashlib.sha256(data_str.encode()).hexdigest()

            if self.use_postgresql:
                cursor.execute(
                    """
                    INSERT INTO raw_data (spreadsheet_id, row_number, data_json, data_hash)
                    VALUES (%s, %s, %s, %s)
                """,
                    (spreadsheet_id, i, data_str, data_hash),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO raw_data (spreadsheet_id, row_number, data_json, data_hash)
                    VALUES (?, ?, ?, ?)
                """,
                    (spreadsheet_id, i, data_str, data_hash),
                )

        conn.commit()
        conn.close()
        print(f"💾 Saved {len(data)} rows for spreadsheet {spreadsheet_id}")

    def create_extraction_job(self, job_name: str) -> int:
        """Create a new extraction job and return its ID."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        if self.use_postgresql:
            cursor.execute(
                """
                INSERT INTO extraction_jobs (job_name, total_spreadsheets)
                VALUES (%s, %s)
                RETURNING id
            """,
                (job_name, len(self.sheet_urls)),
            )
            job_id = cursor.fetchone()["id"]
        else:
            cursor.execute(
                """
                INSERT INTO extraction_jobs (job_name, total_spreadsheets)
                VALUES (?, ?)
            """,
                (job_name, len(self.sheet_urls)),
            )
            job_id = cursor.lastrowid

        conn.commit()
        conn.close()
        return job_id

    def update_extraction_job(self, job_id: int, **kwargs):
        """Update extraction job progress."""
        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        set_clauses = []
        values = []

        placeholder = "%s" if self.use_postgresql else "?"

        for key, value in kwargs.items():
            set_clauses.append(f"{key} = {placeholder}")
            values.append(value)

        if set_clauses:
            values.append(job_id)
            cursor.execute(
                """
                UPDATE extraction_jobs
                SET {", ".join(set_clauses)}
                WHERE id = {placeholder}
            """,
                values,
            )

        conn.commit()
        conn.close()

    def extract_all_data(self):
        """Extract data from all configured spreadsheets."""
        print("🚀 Starting improved data extraction...")

        # Create database
        self.create_database()

        # Create extraction job
        job_name = f"improved_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        job_id = self.create_extraction_job(job_name)

        total_rows = 0
        processed_spreadsheets = 0
        successful_spreadsheets = 0

        try:
            for i, url in enumerate(self.sheet_urls, 1):
                print(f"\n📊 Processing spreadsheet {i}/{len(self.sheet_urls)}")
                print(f"🔗 URL: {url}")

                try:
                    # Extract data
                    data, title = self.download_sheet_data(url)
                    processed_spreadsheets += 1

                    if data:
                        spreadsheet_id = self.extract_spreadsheet_id(url)

                        # Determine sheet type based on title
                        sheet_type = "unknown"
                        title_lower = title.lower()
                        if "survey" in title_lower:
                            sheet_type = "survey"
                        elif "assessment" in title_lower:
                            sheet_type = "assessment"
                        elif "inventory" in title_lower:
                            sheet_type = "inventory"
                        elif "intake" in title_lower:
                            sheet_type = "intake"

                        # Save spreadsheet info
                        self.save_spreadsheet_info(spreadsheet_id, url, title, sheet_type)

                        # Save raw data
                        self.save_raw_data(spreadsheet_id, data)

                        total_rows += len(data)
                        successful_spreadsheets += 1

                        print(f"✅ Successfully processed: {title}")
                    else:
                        print(f"⚠️  No data extracted from: {url}")

                    # Update job progress
                    self.update_extraction_job(
                        job_id,
                        processed_spreadsheets=processed_spreadsheets,
                        successful_spreadsheets=successful_spreadsheets,
                        total_rows=total_rows,
                        processed_rows=total_rows,
                    )

                    # Small delay between requests
                    time.sleep(1)

                except Exception as e:
                    print(f"❌ Error processing spreadsheet {i}: {e}")
                    processed_spreadsheets += 1
                    continue

            # Mark job as completed
            self.update_extraction_job(
                job_id,
                status="completed",
                completed_at=datetime.now(),
                processed_spreadsheets=processed_spreadsheets,
                successful_spreadsheets=successful_spreadsheets,
                total_rows=total_rows,
                processed_rows=total_rows,
            )

            print("\n✅ Extraction completed successfully!")
            print(f"📈 Job ID: {job_id}")
            print(f"📊 Processed {processed_spreadsheets}/{len(self.sheet_urls)} spreadsheets")
            print(f"🎯 Successfully extracted from {successful_spreadsheets} spreadsheets")
            print(f"📝 Total rows extracted: {total_rows}")
            print(f"💾 Database: {self.db_path}")

        except Exception as e:
            # Mark job as failed
            self.update_extraction_job(
                job_id, status="failed", completed_at=datetime.now(), error_message=str(e)
            )
            print(f"❌ Extraction failed: {e}")
            raise

    def show_database_info(self):
        """Show information about the database contents."""
        if not self.use_postgresql and not os.path.exists(self.db_path):
            print(f"❌ Database not found: {self.db_path}")
            return

        conn = self.db_connection.get_connection()
        cursor = conn.cursor()

        print(f"\n📊 Database Information: {self.db_path}")
        print("=" * 60)

        # Show spreadsheets
        cursor.execute("SELECT COUNT(*) FROM spreadsheets")
        spreadsheet_count = cursor.fetchone()[0]
        print(f"📋 Spreadsheets: {spreadsheet_count}")

        # Show raw data
        cursor.execute("SELECT COUNT(*) FROM raw_data")
        row_count = cursor.fetchone()[0]
        print(f"📝 Total rows: {row_count}")

        # Show extraction jobs
        cursor.execute("SELECT COUNT(*) FROM extraction_jobs")
        job_count = cursor.fetchone()[0]
        print(f"🔄 Extraction jobs: {job_count}")

        # Show recent jobs
        cursor.execute(
            """
            SELECT id, job_name, status, successful_spreadsheets, total_spreadsheets, total_rows, started_at
            FROM extraction_jobs
            ORDER BY started_at DESC
            LIMIT 3
        """
        )

        jobs = cursor.fetchall()
        if jobs:
            print("\n📋 Recent extraction jobs:")
            for job in jobs:
                job_id, name, status, successful, total_sheets, total_rows, started = job
                print(f"  • Job {job_id}: {name}")
                print(
                    f"    Status: {status} | Success: {successful}/{total_sheets} sheets | Rows: {total_rows} | Started: {started}"
                )

        # Show spreadsheet details
        cursor.execute(
            """
            SELECT s.spreadsheet_id, s.title, s.sheet_type, COUNT(r.id) as row_count, s.last_synced
            FROM spreadsheets s
            LEFT JOIN raw_data r ON s.spreadsheet_id = r.spreadsheet_id
            GROUP BY s.spreadsheet_id, s.title, s.sheet_type, s.last_synced
            ORDER BY s.last_synced DESC
        """
        )

        spreadsheets = cursor.fetchall()
        if spreadsheets:
            print("\n📊 Spreadsheet details:")
            for sheet in spreadsheets:
                sheet_id, title, sheet_type, rows, synced = sheet
                print(f"  • {sheet_id}: {title}")
                print(f"    Type: {sheet_type} | Rows: {rows} | Last synced: {synced}")

        conn.close()


def main():
    """Main function to run the improved data extraction."""
    print("🔍 Improved Google Sheets Data Extractor")
    print("=" * 50)

    extractor = ImprovedExtractor()

    try:
        # Extract all data
        extractor.extract_all_data()

        # Show database info
        extractor.show_database_info()

    except KeyboardInterrupt:
        print("\n⚠️  Extraction cancelled by user")
    except Exception as e:
        print(f"\n❌ Extraction failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
