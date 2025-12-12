#!/usr/bin/env python3
"""
Auto-Sync Service for Survey Data

Automatically detects and imports new spreadsheet data when changes are detected.
Can be run as a standalone service or integrated into the Flask application.

Supports both SQLite (local) and PostgreSQL (production) via DATABASE_URL.
"""

import logging
import os
import threading
import time
from datetime import datetime, timedelta
from typing import Any, Dict

from db_utils import is_postgresql

from src.normalizers.survey_normalizer import SurveyNormalizer

logger = logging.getLogger(__name__)


class AutoSyncService:
    """Service for automatically syncing survey data."""

    def __init__(
        self,
        source_db: str = "surveyor_data_improved.db",
        target_db: str = "survey_normalized.db",
        check_interval: int = 300,
    ):  # 5 minutes default
        self.source_db = source_db
        self.target_db = target_db
        self.check_interval = check_interval
        self.use_postgresql = is_postgresql()

        # When using PostgreSQL, both source and target use the same database
        # The normalizer will handle the database connections appropriately
        self.normalizer = SurveyNormalizer(source_db, target_db)

        self.running = False
        self.thread = None
        self.last_check = None
        self.sync_stats = {
            "total_syncs": 0,
            "successful_syncs": 0,
            "failed_syncs": 0,
            "last_sync_time": None,
            "last_error": None,
        }

        db_type = (
            "PostgreSQL"
            if self.use_postgresql
            else f"SQLite (source={source_db}, target={target_db})"
        )
        logger.info(f"AutoSyncService initialized with {db_type}")

    def _ensure_schema_exists(self):
        """Ensure database schema exists (create if missing)."""
        if self.use_postgresql:
            # For PostgreSQL, check if sync_tracking table exists
            try:
                conn = self.normalizer.target_db_connection.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM sync_tracking LIMIT 1")
                conn.close()
                logger.info("✅ Database schema already exists")
            except Exception:
                # Table doesn't exist, create schema
                logger.info("📊 Creating normalized database schema in PostgreSQL...")
                print("📊 Creating normalized database structure...")
                self.normalizer.create_normalized_schema()
                logger.info("✅ Database schema created successfully")
        elif not os.path.exists(self.target_db):
            # For SQLite, check if file exists
            logger.info("📊 Creating normalized database structure...")
            print("📊 Creating normalized database structure...")
            self.normalizer.create_normalized_schema()
            logger.info("✅ Database schema created successfully")
        else:
            logger.info("✅ Database schema already exists")

    def start(self):
        """Start the auto-sync service."""
        if self.running:
            print("⚠️  Auto-sync service is already running")
            return

        print(f"🚀 Starting auto-sync service (checking every {self.check_interval} seconds)")

        # Ensure database schema exists before starting sync loop
        self._ensure_schema_exists()

        self.running = True
        self.thread = threading.Thread(target=self._sync_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop the auto-sync service."""
        if not self.running:
            print("⚠️  Auto-sync service is not running")
            return

        print("🛑 Stopping auto-sync service...")
        self.running = False
        if self.thread:
            self.thread.join(timeout=10)
        print("✅ Auto-sync service stopped")

    def _sync_loop(self):
        """Main sync loop that runs in a separate thread."""
        while self.running:
            try:
                self._perform_sync_check()
                time.sleep(self.check_interval)
            except Exception as e:
                print(f"❌ Error in sync loop: {e}")
                self.sync_stats["failed_syncs"] += 1
                self.sync_stats["last_error"] = str(e)
                time.sleep(self.check_interval)

    def _perform_sync_check(self):
        """Perform a single sync check."""
        self.last_check = datetime.now()

        # For SQLite, check if source database exists
        if not self.use_postgresql and not os.path.exists(self.source_db):
            logger.debug(f"Source database {self.source_db} does not exist, skipping sync")
            return

        # Ensure target database schema exists (both SQLite and PostgreSQL)
        if self.use_postgresql:
            # For PostgreSQL, check if sync_tracking table exists
            try:
                conn = self.normalizer.target_db_connection.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM sync_tracking LIMIT 1")
                conn.close()
            except Exception:
                # Table doesn't exist, create schema
                logger.info("📊 Creating normalized database schema in PostgreSQL...")
                print("📊 Creating normalized database structure...")
                self.normalizer.create_normalized_schema()
        elif not os.path.exists(self.target_db):
            # For SQLite, check if file exists
            print("📊 Creating normalized database structure...")
            self.normalizer.create_normalized_schema()

        try:
            # Check for new data
            changes = self.normalizer.check_for_new_data()

            if changes["total_changes"] > 0:
                print(f"🔄 Auto-sync detected {changes['total_changes']} changes")
                result = self.normalizer.auto_import_new_data()

                self.sync_stats["total_syncs"] += 1
                if result["total_processed"] > 0:
                    self.sync_stats["successful_syncs"] += 1
                    self.sync_stats["last_sync_time"] = datetime.now()
                    print(f"✅ Auto-sync completed: {result['message']}")
                else:
                    print(f"ℹ️  Auto-sync: {result['message']}")

        except Exception as e:
            self.sync_stats["failed_syncs"] += 1
            self.sync_stats["last_error"] = str(e)
            print(f"❌ Auto-sync failed: {e}")

    def force_sync(self) -> Dict[str, Any]:
        """Force an immediate sync check."""
        print("🔄 Forcing immediate sync check...")
        try:
            self._perform_sync_check()
            return {"success": True, "message": "Sync check completed", "stats": self.get_stats()}
        except Exception as e:
            return {"success": False, "message": f"Sync failed: {e}", "stats": self.get_stats()}

    def get_stats(self) -> Dict[str, Any]:
        """Get sync service statistics."""
        return {
            "running": self.running,
            "check_interval": self.check_interval,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "sync_stats": self.sync_stats.copy(),
            "next_check": (
                (self.last_check + timedelta(seconds=self.check_interval)).isoformat()
                if self.last_check
                else None
            ),
        }

    def get_sync_status(self) -> Dict[str, Any]:
        """Get current sync status for dashboard display."""
        try:
            changes = self.normalizer.check_for_new_data()

            # Get sync tracking info - use normalizer's target connection
            conn = self.normalizer.target_db_connection.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    COUNT(*) as total_tracked,
                    COUNT(CASE WHEN sync_status = 'completed' THEN 1 END) as completed,
                    COUNT(CASE WHEN sync_status = 'failed' THEN 1 END) as failed,
                    MAX(last_sync_timestamp) as last_sync
                FROM sync_tracking
            """
            )

            tracking_stats = cursor.fetchone()
            conn.close()

            # Handle both dict (PostgreSQL) and tuple (SQLite) results
            if isinstance(tracking_stats, dict):
                total_tracked = tracking_stats.get("total_tracked", 0)
                completed = tracking_stats.get("completed", 0)
                failed = tracking_stats.get("failed", 0)
                last_sync = tracking_stats.get("last_sync")
            else:
                total_tracked = tracking_stats[0] if tracking_stats else 0
                completed = tracking_stats[1] if tracking_stats else 0
                failed = tracking_stats[2] if tracking_stats else 0
                last_sync = tracking_stats[3] if tracking_stats else None

            return {
                "pending_changes": changes["total_changes"],
                "new_spreadsheets": len(changes["new_data"]),
                "updated_spreadsheets": len(changes["updated_data"]),
                "total_tracked": total_tracked,
                "completed_syncs": completed,
                "failed_syncs": failed,
                "last_sync": last_sync,
                "service_stats": self.get_stats(),
            }

        except Exception as e:
            return {"error": str(e), "service_stats": self.get_stats()}


# Global auto-sync service instance
_auto_sync_service = None


def get_auto_sync_service() -> AutoSyncService:
    """Get the global auto-sync service instance."""
    global _auto_sync_service
    if _auto_sync_service is None:
        _auto_sync_service = AutoSyncService()
    return _auto_sync_service


def start_auto_sync(check_interval: int = 300):
    """Start the auto-sync service with specified interval."""
    service = get_auto_sync_service()
    service.check_interval = check_interval
    service.start()
    return service


def stop_auto_sync():
    """Stop the auto-sync service."""
    service = get_auto_sync_service()
    service.stop()


def main():
    """Run the auto-sync service as a standalone application."""
    import signal
    import sys

    # Parse command line arguments
    check_interval = 300  # 5 minutes default

    if len(sys.argv) > 1:
        try:
            check_interval = int(sys.argv[1])
        except ValueError:
            print("Usage: python auto_sync_service.py [check_interval_seconds]")
            return 1

    print("🔄 Survey Auto-Sync Service")
    print("=" * 50)
    print("📊 Source DB: surveyor_data_improved.db")
    print("💾 Target DB: survey_normalized.db")
    print(f"⏱️  Check interval: {check_interval} seconds")
    print()

    # Create and start service
    service = AutoSyncService(check_interval=check_interval)

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n🛑 Received interrupt signal")
        service.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start the service
    service.start()

    try:
        # Keep the main thread alive
        while service.running:
            time.sleep(1)
    except KeyboardInterrupt:
        service.stop()

    return 0


if __name__ == "__main__":
    exit(main())
