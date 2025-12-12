"""
Dependency Injection Container for JJF Survey Analytics.

Provides centralized service instance management with:
- Singleton pattern for container
- Lazy initialization of services and repositories
- Thread-safe service creation
- Clear dependency injection

Example:
    container = get_container()
    data_service = container.data_service
    analytics_service = container.analytics_service  # Gets DataService injected
"""

import os
import threading
from typing import Optional

# Import all repositories
from src.repositories import (
    AdminEditRepository,
    ReportRepository,
    SheetRepository,
    get_admin_edit_repository,
    get_report_repository,
    get_sheet_repository,
)
from src.services.admin_edit_service import AdminEditService, get_admin_edit_service
from src.services.algorithm_config_service import (
    AlgorithmConfigService,
    get_algorithm_config_service,
)
from src.services.analytics_service import AnalyticsService, get_analytics_service

# Import all services
from src.services.cache_service import CacheService, get_cache_service
from src.services.data_service import DataService, get_data_service
from src.services.report_generator import ReportGenerator
from src.services.report_service import ReportService


class Container:
    """
    Dependency injection container for all application services and repositories.

    Manages service lifecycle and dependencies using lazy initialization.
    Thread-safe singleton pattern ensures consistent state across application.
    """

    def __init__(self):
        """Initialize container with locks for thread-safe lazy loading."""
        self._lock = threading.RLock()

        # Repository instances (lazy-initialized)
        self._sheet_repository: Optional[SheetRepository] = None
        self._report_repository: Optional[ReportRepository] = None
        self._admin_edit_repository: Optional[AdminEditRepository] = None

        # Service instances (lazy-initialized)
        self._cache_service: Optional[CacheService] = None
        self._data_service: Optional[DataService] = None
        self._admin_edit_service: Optional[AdminEditService] = None
        self._analytics_service: Optional[AnalyticsService] = None
        self._algorithm_config_service: Optional[AlgorithmConfigService] = None
        self._report_generator: Optional[ReportGenerator] = None
        self._report_service: Optional[ReportService] = None

    # Repository Properties

    @property
    def sheet_repository(self) -> SheetRepository:
        """
        Get or create SheetRepository instance (thread-safe singleton).

        Returns:
            SheetRepository singleton instance
        """
        if self._sheet_repository is None:
            with self._lock:
                if self._sheet_repository is None:
                    self._sheet_repository = get_sheet_repository()
        return self._sheet_repository

    @property
    def report_repository(self) -> ReportRepository:
        """
        Get or create ReportRepository instance (thread-safe singleton).

        Returns:
            ReportRepository singleton instance
        """
        if self._report_repository is None:
            with self._lock:
                if self._report_repository is None:
                    self._report_repository = get_report_repository()
        return self._report_repository

    @property
    def admin_edit_repository(self) -> AdminEditRepository:
        """
        Get or create AdminEditRepository instance (thread-safe singleton).

        Returns:
            AdminEditRepository singleton instance
        """
        if self._admin_edit_repository is None:
            with self._lock:
                if self._admin_edit_repository is None:
                    self._admin_edit_repository = get_admin_edit_repository()
        return self._admin_edit_repository

    # Service Properties

    @property
    def cache_service(self) -> CacheService:
        """
        Get or create CacheService with ReportRepository dependency (thread-safe).

        Returns:
            CacheService singleton instance with injected dependencies
        """
        if self._cache_service is None:
            with self._lock:
                if self._cache_service is None:
                    self._cache_service = get_cache_service(
                        report_repository=self.report_repository
                    )
        return self._cache_service

    @property
    def data_service(self) -> DataService:
        """
        Get or create DataService with SheetRepository dependency (thread-safe).

        Returns:
            DataService singleton instance with injected dependencies
        """
        if self._data_service is None:
            with self._lock:
                if self._data_service is None:
                    self._data_service = get_data_service(sheet_repository=self.sheet_repository)
        return self._data_service

    @property
    def admin_edit_service(self) -> AdminEditService:
        """
        Get or create AdminEditService with AdminEditRepository dependency (thread-safe).

        Returns:
            AdminEditService singleton instance with injected dependencies
        """
        if self._admin_edit_service is None:
            with self._lock:
                if self._admin_edit_service is None:
                    self._admin_edit_service = get_admin_edit_service(
                        admin_edit_repository=self.admin_edit_repository
                    )
        return self._admin_edit_service

    @property
    def analytics_service(self) -> AnalyticsService:
        """
        Get or create AnalyticsService with DataService dependency (thread-safe).

        Demonstrates dependency injection pattern: AnalyticsService requires
        DataService, which is automatically injected by the container.

        Returns:
            AnalyticsService singleton instance with injected dependencies
        """
        if self._analytics_service is None:
            with self._lock:
                if self._analytics_service is None:
                    # Inject DataService dependency
                    self._analytics_service = get_analytics_service(data_service=self.data_service)
        return self._analytics_service

    @property
    def algorithm_config_service(self) -> AlgorithmConfigService:
        """
        Get or create AlgorithmConfigService instance (thread-safe singleton).

        Returns:
            AlgorithmConfigService singleton instance
        """
        if self._algorithm_config_service is None:
            with self._lock:
                if self._algorithm_config_service is None:
                    self._algorithm_config_service = get_algorithm_config_service()
        return self._algorithm_config_service

    @property
    def report_generator(self) -> ReportGenerator:
        """
        Get or create ReportGenerator with dependencies (thread-safe).

        Returns:
            ReportGenerator instance with sheet data and admin edits
        """
        if self._report_generator is None:
            with self._lock:
                if self._report_generator is None:
                    # Get sheet data from DataService
                    sheet_data = self.data_service.get_all_data()
                    # Get admin edits from AdminEditService
                    admin_edits = self.admin_edit_service.get_all_edits()

                    # Auto-detect AI availability from environment
                    enable_ai = bool(os.getenv("OPENROUTER_API_KEY"))

                    self._report_generator = ReportGenerator(
                        sheet_data=sheet_data,
                        enable_ai=enable_ai,  # Auto-detect from environment
                        admin_edits=admin_edits,
                    )
        return self._report_generator

    @property
    def report_service(self) -> ReportService:
        """
        Get or create ReportService with dependencies (thread-safe).

        Returns:
            ReportService instance with generator and supporting services
        """
        if self._report_service is None:
            with self._lock:
                if self._report_service is None:
                    self._report_service = ReportService(
                        report_generator=self.report_generator,
                        data_service=self.data_service,
                        admin_edit_service=self.admin_edit_service,
                        cache_service=self.cache_service,
                    )
        return self._report_service

    def reset(self) -> None:
        """
        Reset all services and repositories (useful for testing).

        Clears all instances, forcing re-initialization on next access.
        """
        with self._lock:
            # Reset repositories
            self._sheet_repository = None
            self._report_repository = None
            self._admin_edit_repository = None

            # Reset services
            self._cache_service = None
            self._data_service = None
            self._admin_edit_service = None
            self._analytics_service = None
            self._algorithm_config_service = None
            self._report_generator = None
            self._report_service = None

    def get_status(self) -> dict:
        """
        Get container status showing which services and repositories are initialized.

        Returns:
            Dictionary mapping component names to initialization status
        """
        return {
            # Repositories
            "sheet_repository": self._sheet_repository is not None,
            "report_repository": self._report_repository is not None,
            "admin_edit_repository": self._admin_edit_repository is not None,
            # Services
            "cache_service": self._cache_service is not None,
            "data_service": self._data_service is not None,
            "admin_edit_service": self._admin_edit_service is not None,
            "analytics_service": self._analytics_service is not None,
            "algorithm_config_service": self._algorithm_config_service is not None,
            "report_generator": self._report_generator is not None,
            "report_service": self._report_service is not None,
        }


# Global container instance
_container: Optional[Container] = None
_container_lock = threading.RLock()


def get_container() -> Container:
    """
    Get the global Container instance (thread-safe singleton).

    Returns:
        Container singleton instance
    """
    global _container
    if _container is None:
        with _container_lock:
            if _container is None:
                _container = Container()
    return _container


def reset_container() -> None:
    """
    Reset the global container (useful for testing).

    Clears the global container instance, forcing re-creation on next access.
    """
    global _container
    with _container_lock:
        _container = None
