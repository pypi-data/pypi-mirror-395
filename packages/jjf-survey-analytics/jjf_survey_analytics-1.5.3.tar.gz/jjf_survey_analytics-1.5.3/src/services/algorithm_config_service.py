"""
Algorithm Configuration Service for JJF Survey Analytics.

Manages algorithm configuration (maturity rubric, scoring weights) with JSON persistence.
Provides thread-safe configuration updates, backup management, and version tracking.

Key Features:
- Load/save algorithm configuration from JSON file
- Automatic backup creation with rotation (keep last 10)
- Configuration validation hooks
- Thread-safe operations
- Deep copy for data isolation
- Singleton pattern for global access

Example:
    service = get_algorithm_config_service()
    config = service.get_config()
    service.update_config({"version": "1.1.0", ...})
    service.create_backup()
"""

import glob
import json
import os
import threading
from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from src.validators.algorithm_validator import get_algorithm_validator

# Default algorithm configuration
DEFAULT_CONFIG = {
    "version": 1,
    "algorithm_config": {
        "maturity_assessment": {
            "variance_thresholds": {
                "low": {"max": 0.5, "color": "#22c55e", "label": "Low Variance"},
                "medium": {"max": 1.0, "color": "#eab308", "label": "Medium Variance"},
                "high": {"color": "#ef4444", "label": "High Variance"},
            },
            "maturity_levels": {
                "1_building": {
                    "score_range": {"min": 0, "max": 35},
                    "percentage_range": {"min": 0, "max": 35},
                    "color": "#ef4444",
                    "name": "Building",
                },
                "2_emerging": {
                    "score_range": {"min": 36, "max": 70},
                    "percentage_range": {"min": 36, "max": 70},
                    "color": "#eab308",
                    "name": "Emerging",
                },
                "3_thriving": {
                    "score_range": {"min": 71, "max": 100},
                    "percentage_range": {"min": 71, "max": 100},
                    "color": "#22c55e",
                    "name": "Thriving",
                },
            },
            "dimension_weights": {
                "program_technology": 0.2,
                "business_systems": 0.2,
                "data_analytics": 0.2,
                "infrastructure": 0.2,
                "organizational_culture": 0.2,
            },
        },
        "scoring": {"valid_score_range": {"min": 1, "max": 5}},
    },
}


class AlgorithmConfigService:
    """
    Service for managing algorithm configuration with JSON persistence.

    Provides thread-safe configuration management with backup/restore capabilities.
    Uses singleton pattern to ensure single source of truth for configuration.
    """

    def __init__(self, config_path: str = "algorithm_config.json"):
        """
        Initialize AlgorithmConfigService.

        Args:
            config_path: Path to configuration JSON file
        """
        self._config_path = config_path
        self._config: Dict[str, Any] = {}
        self._lock = threading.RLock()
        self._load_count = 0
        self._last_load_time: Optional[datetime] = None
        self._last_save_time: Optional[datetime] = None
        self._history: List[Dict[str, Any]] = []

        # Load configuration on initialization
        self._load_config()

    def _load_config(self) -> None:
        """
        Load configuration from JSON file.

        If file doesn't exist, creates it with default configuration.
        Thread-safe with deep copy for isolation.
        """
        with self._lock:
            if os.path.exists(self._config_path):
                try:
                    with open(self._config_path, "r", encoding="utf-8") as f:
                        loaded_config = json.load(f)
                        self._config = deepcopy(loaded_config)
                        self._load_count += 1
                        self._last_load_time = datetime.now()
                except (json.JSONDecodeError, IOError) as e:
                    # If load fails, use default config
                    self._config = deepcopy(DEFAULT_CONFIG)
                    self._save_config()
                    raise ValueError(f"Failed to load config from {self._config_path}: {e}")
            else:
                # Create new config file with defaults
                self._config = deepcopy(DEFAULT_CONFIG)
                self._save_config()
                self._load_count += 1
                self._last_load_time = datetime.now()

    def _save_config(self) -> None:
        """
        Save current configuration to JSON file.

        Thread-safe write operation with error handling.
        """
        with self._lock:
            try:
                with open(self._config_path, "w", encoding="utf-8") as f:
                    json.dump(self._config, f, indent=2)
                self._last_save_time = datetime.now()
            except IOError as e:
                raise ValueError(f"Failed to save config to {self._config_path}: {e}")

    def get_config(self) -> Dict[str, Any]:
        """
        Get current algorithm configuration.

        Returns:
            Deep copy of current configuration dictionary
        """
        with self._lock:
            return deepcopy(self._config)

    def update_config(
        self, new_config: Dict[str, Any], validate: bool = True
    ) -> Tuple[bool, Optional[Dict]]:
        """
        Update algorithm configuration.

        Args:
            new_config: New configuration dictionary
            validate: Whether to validate configuration (default: True)

        Returns:
            Tuple of (success: bool, validation_result: Optional[Dict])
            If validation fails, returns (False, validation_result_dict)
            If successful, returns (True, None)
        """
        with self._lock:
            # Validate configuration using AlgorithmValidator
            if validate:
                validator = get_algorithm_validator()
                validation_result = validator.validate(new_config)

                if not validation_result.valid:
                    return False, validation_result.to_dict()

            # Store old config in history before updating
            history_entry = {
                "timestamp": datetime.now().isoformat(),
                "old_config": deepcopy(self._config),
                "new_config": deepcopy(new_config),
            }
            self._history.append(history_entry)

            # Update config
            self._config = deepcopy(new_config)

            # Save to file
            self._save_config()

            return True, None

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get configuration change history.

        Returns:
            List of history entries (deep copies)
        """
        with self._lock:
            return deepcopy(self._history)

    def create_backup(self) -> str:
        """
        Create timestamped backup of current configuration.

        Returns:
            Filename of created backup
        """
        with self._lock:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"algorithm_config_backup_{timestamp}.json"

            try:
                with open(backup_filename, "w", encoding="utf-8") as f:
                    json.dump(self._config, f, indent=2)

                # Rotate backups (keep last 10)
                self._rotate_backups()

                return backup_filename
            except IOError as e:
                raise ValueError(f"Failed to create backup {backup_filename}: {e}")

    def _rotate_backups(self, max_backups: int = 10) -> None:
        """
        Rotate backup files, keeping only the most recent max_backups.

        Args:
            max_backups: Maximum number of backups to keep (default: 10)
        """
        # Find all backup files
        backup_files = glob.glob("algorithm_config_backup_*.json")

        # Sort by modification time (oldest first)
        backup_files.sort(key=os.path.getmtime)

        # Remove oldest files if we exceed max_backups
        while len(backup_files) > max_backups:
            oldest_file = backup_files.pop(0)
            try:
                os.remove(oldest_file)
            except OSError:
                pass  # Ignore errors during rotation

    def get_backup(self, filename: str) -> Dict[str, Any]:
        """
        Load specific backup file.

        Args:
            filename: Backup filename to load

        Returns:
            Configuration dictionary from backup

        Raises:
            ValueError: If backup file doesn't exist or is invalid
        """
        if not os.path.exists(filename):
            raise ValueError(f"Backup file not found: {filename}")

        try:
            with open(filename, "r", encoding="utf-8") as f:
                backup_config = json.load(f)
                return deepcopy(backup_config)
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"Failed to load backup {filename}: {e}")

    def restore_backup(self, filename: str) -> bool:
        """
        Restore configuration from backup file.

        Args:
            filename: Backup filename to restore from

        Returns:
            True if restore successful

        Raises:
            ValueError: If backup file is invalid or fails validation
        """
        backup_config = self.get_backup(filename)
        success, error = self.update_config(backup_config, validate=True)

        if not success:
            raise ValueError(f"Backup configuration is invalid: {error}")

        return True

    def list_backups(self) -> List[str]:
        """
        List available backup files.

        Returns:
            List of backup filenames, sorted by modification time (newest first)
        """
        backup_files = glob.glob("algorithm_config_backup_*.json")
        # Sort by modification time (newest first)
        backup_files.sort(key=os.path.getmtime, reverse=True)
        return backup_files

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get service metadata.

        Returns:
            Dictionary containing load count, timestamps, etc.
        """
        with self._lock:
            return {
                "config_path": self._config_path,
                "load_count": self._load_count,
                "last_load_time": (
                    self._last_load_time.isoformat() if self._last_load_time else None
                ),
                "last_save_time": (
                    self._last_save_time.isoformat() if self._last_save_time else None
                ),
                "history_count": len(self._history),
                "backup_count": len(self.list_backups()),
            }


# Global singleton instance
_algorithm_config_service: Optional[AlgorithmConfigService] = None
_algorithm_config_service_lock = threading.RLock()


def get_algorithm_config_service(
    config_path: str = "algorithm_config.json",
) -> AlgorithmConfigService:
    """
    Get the global AlgorithmConfigService instance (thread-safe singleton).

    Args:
        config_path: Path to configuration JSON file (only used on first call)

    Returns:
        AlgorithmConfigService singleton instance
    """
    global _algorithm_config_service
    if _algorithm_config_service is None:
        with _algorithm_config_service_lock:
            if _algorithm_config_service is None:
                _algorithm_config_service = AlgorithmConfigService(config_path)
    return _algorithm_config_service


def reset_algorithm_config_service() -> None:
    """
    Reset the global AlgorithmConfigService instance (useful for testing).
    """
    global _algorithm_config_service
    with _algorithm_config_service_lock:
        _algorithm_config_service = None
