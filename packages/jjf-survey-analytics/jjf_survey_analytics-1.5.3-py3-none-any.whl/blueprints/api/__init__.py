"""
API Blueprints package for JJF Survey Analytics.

Organizes all API endpoints into focused, modular blueprints.
"""

from src.blueprints.api.admin_edit_api import admin_edit_api
from src.blueprints.api.algorithm_config_api import algorithm_config_api
from src.blueprints.api.cache_api import cache_api

# Import all API blueprints for easy access
from src.blueprints.api.data_api import data_api
from src.blueprints.api.help_api import help_api
from src.blueprints.api.report_api import report_api
from src.blueprints.api.stats_api import stats_api
from src.blueprints.api.whats_new_api import whats_new_api

__all__ = [
    "data_api",
    "report_api",
    "cache_api",
    "stats_api",
    "admin_edit_api",
    "algorithm_config_api",
    "help_api",
    "whats_new_api",
]
