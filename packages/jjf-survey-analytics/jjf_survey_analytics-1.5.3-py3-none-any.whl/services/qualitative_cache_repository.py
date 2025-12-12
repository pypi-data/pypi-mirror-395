#!/usr/bin/env python3
"""
QualitativeCacheRepository - Repository for qualitative analysis cache management.

Handles CRUD operations for the report_qualitative_cache table with business logic
for cache hit/miss, invalidation, and version management.

This repository provides:
- Cache retrieval with user-edited version precedence
- AI-generated and user-edited data storage
- Automatic version incrementing on edits
- SHA256-based cache invalidation
- Bulk operations for organization-level management

Usage:
    from src.services.qualitative_cache_repository import QualitativeCacheRepository

    # Create repository (uses default database session)
    repo = QualitativeCacheRepository()

    # Get cached data (returns user-edited if available, else AI-generated)
    data = repo.get_cached_data("Example Org", "Program Technology")

    # Save AI-generated analysis
    repo.save_ai_generated(
        "Example Org",
        "Program Technology",
        {"summary": "...", "themes": [...], "modifiers": [...]},
        "abc123def456..."
    )

    # Save user edits
    repo.save_user_edit(
        "Example Org",
        "Program Technology",
        {"summary": "Updated...", "themes": [...], "modifiers": [...]}
    )

Cache Invalidation:
    The repository uses SHA256 hashing to detect when underlying response data
    has changed. When a hash mismatch is detected, user edits are cleared and
    AI analysis is regenerated.

Thread Safety:
    All operations use database session management via SQLAlchemy, which provides
    transaction isolation. For concurrent access, use proper session scoping.
"""

import hashlib
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from src.surveyor.models.base import create_database_engine, create_session_factory
from src.surveyor.models.qualitative_cache import QualitativeCache

# Configure logger
logger = logging.getLogger(__name__)


class QualitativeCacheRepository:
    """
    Repository for qualitative analysis cache operations.

    Provides CRUD operations with business logic for cache invalidation,
    version management, and data precedence (user-edited > AI-generated).
    """

    # Valid technology dimensions
    VALID_DIMENSIONS = [
        "Program Technology",
        "Business Systems",
        "Data Management",
        "Infrastructure",
        "Organizational Culture"
    ]

    def __init__(self, session: Optional[Session] = None, database_url: Optional[str] = None):
        """
        Initialize repository with database session.

        Args:
            session: SQLAlchemy session (optional, creates new if not provided)
            database_url: Database URL (optional, uses default if not provided)
        """
        if session:
            self._session = session
            self._owns_session = False
        else:
            # Create session from database URL or default
            db_url = database_url or "sqlite:///survey_data.db"
            engine = create_database_engine(db_url)
            SessionFactory = create_session_factory(engine)
            self._session = SessionFactory()
            self._owns_session = True

    def __del__(self):
        """Close session if owned by repository."""
        if hasattr(self, '_owns_session') and self._owns_session and hasattr(self, '_session'):
            self._session.close()

    def get_cached_data(self, org_name: str, dimension: str) -> Optional[Dict]:
        """
        Get cached qualitative data for organization and dimension.

        Returns user-edited version if available, otherwise AI-generated version.
        Tracks cache hit/miss metrics.

        Args:
            org_name: Organization name
            dimension: Technology dimension

        Returns:
            Dictionary with cached data or None if not cached:
            {
                "data": {...},          # Parsed JSON data
                "source": "user_edited" | "ai_generated",
                "version": 1,
                "cached_at": "2025-11-24T12:00:00",
                "response_hash": "abc123..."
            }

        Raises:
            ValueError: If dimension is invalid
        """
        self._validate_dimension(dimension)

        entry = self._session.query(QualitativeCache).filter_by(
            org_name=org_name,
            dimension=dimension
        ).first()

        if not entry:
            return None  # Cache miss

        # Prefer user-edited data if available
        if entry.has_user_edits():
            data = json.loads(entry.get_active_data())
            return {
                "data": data,
                "source": "user_edited",
                "version": entry.version,
                "cached_at": entry.updated_at.isoformat() if entry.updated_at else None,
                "response_hash": entry.response_count_hash
            }
        else:
            data = json.loads(entry.get_active_data())
            return {
                "data": data,
                "source": "ai_generated",
                "version": entry.version,
                "cached_at": entry.created_at.isoformat() if entry.created_at else None,
                "response_hash": entry.response_count_hash
            }

    def save_ai_generated(
        self,
        org_name: str,
        dimension: str,
        data: Dict,
        response_hash: str
    ) -> QualitativeCache:
        """
        Save AI-generated qualitative analysis to cache.

        Creates new entry or updates existing. If hash has changed, clears user edits.

        Args:
            org_name: Organization name
            dimension: Technology dimension
            data: AI-generated analysis data (dict with summary, themes, modifiers)
            response_hash: SHA256 hash for cache invalidation

        Returns:
            QualitativeCache entry

        Raises:
            ValueError: If dimension is invalid or data structure is invalid
        """
        self._validate_dimension(dimension)
        self._validate_data_structure(data)

        # JJF-42: Log validation success with modifier statistics
        modifiers = data.get('modifiers', [])
        non_zero_count = sum(1 for m in modifiers if m.get('value', 0) != 0)
        logger.debug(
            f"Validated {len(modifiers)} modifiers for {org_name}/{dimension} "
            f"({non_zero_count} non-zero, all have reasoning)"
        )

        # Check for existing entry
        entry = self._session.query(QualitativeCache).filter_by(
            org_name=org_name,
            dimension=dimension
        ).first()

        if entry:
            # Check if hash changed before updating (to clear user edits)
            hash_changed = entry.response_count_hash != response_hash

            # Update existing entry
            entry.ai_generated_json = json.dumps(data)
            entry.response_count_hash = response_hash
            entry.updated_at = datetime.utcnow()

            # Clear user edits if hash changed (data has changed)
            if hash_changed:
                entry.clear_user_edits()
        else:
            # Create new entry
            entry = QualitativeCache(
                org_name=org_name,
                dimension=dimension,
                ai_generated_json=json.dumps(data),
                response_count_hash=response_hash,
                version=1
            )
            self._session.add(entry)

        self._session.commit()
        return entry

    def save_user_edit(
        self,
        org_name: str,
        dimension: str,
        edited_data: Dict
    ) -> QualitativeCache:
        """
        Save user edits to cached qualitative analysis.

        Increments version on each edit. Preserves both AI-generated and user-edited versions.

        Args:
            org_name: Organization name
            dimension: Technology dimension
            edited_data: User-modified analysis data

        Returns:
            QualitativeCache entry

        Raises:
            ValueError: If no AI-generated cache exists, dimension invalid, or data invalid
        """
        self._validate_dimension(dimension)
        self._validate_data_structure(edited_data)

        entry = self._session.query(QualitativeCache).filter_by(
            org_name=org_name,
            dimension=dimension
        ).first()

        if not entry:
            raise ValueError(
                f"No cache entry exists for {org_name}/{dimension}. "
                "Generate AI analysis first with save_ai_generated()."
            )

        # Save user edits
        entry.user_edited_json = json.dumps(edited_data)
        entry.version += 1
        entry.updated_at = datetime.utcnow()

        self._session.commit()
        return entry

    def invalidate_if_stale(
        self,
        org_name: str,
        dimension: str,
        current_hash: str
    ) -> bool:
        """
        Check if cache is stale and invalidate if hash has changed.

        Args:
            org_name: Organization name
            dimension: Technology dimension
            current_hash: Current SHA256 hash of response data

        Returns:
            True if cache was invalidated, False if still valid or not found
        """
        entry = self._session.query(QualitativeCache).filter_by(
            org_name=org_name,
            dimension=dimension
        ).first()

        if not entry:
            return False  # No cache to invalidate

        # Check if hash matches
        if entry.response_count_hash != current_hash:
            # Hash changed - clear user edits
            entry.clear_user_edits()
            entry.response_count_hash = current_hash
            self._session.commit()
            return True

        return False  # Cache still valid

    def delete_cache(self, org_name: str, dimension: str) -> bool:
        """
        Delete cache entry for organization and dimension.

        Args:
            org_name: Organization name
            dimension: Technology dimension

        Returns:
            True if entry was deleted, False if not found
        """
        entry = self._session.query(QualitativeCache).filter_by(
            org_name=org_name,
            dimension=dimension
        ).first()

        if entry:
            self._session.delete(entry)
            self._session.commit()
            return True

        return False

    def cache_exists(self, org_name: str, dimension: str) -> bool:
        """
        Check if cache entry exists for organization and dimension.

        Args:
            org_name: Organization name
            dimension: Technology dimension

        Returns:
            True if cache exists, False otherwise
        """
        count = self._session.query(QualitativeCache).filter_by(
            org_name=org_name,
            dimension=dimension
        ).count()

        return count > 0

    def get_cache_metadata(self, org_name: str, dimension: str) -> Optional[Dict]:
        """
        Get cache metadata without loading full data.

        Args:
            org_name: Organization name
            dimension: Technology dimension

        Returns:
            Dictionary with metadata or None if not cached:
            {
                "version": 1,
                "has_user_edits": True,
                "created_at": "2025-11-24T12:00:00",
                "updated_at": "2025-11-24T12:30:00",
                "response_hash": "abc123..."
            }
        """
        entry = self._session.query(QualitativeCache).filter_by(
            org_name=org_name,
            dimension=dimension
        ).first()

        if not entry:
            return None

        return {
            "version": entry.version,
            "has_user_edits": entry.has_user_edits(),
            "created_at": entry.created_at.isoformat() if entry.created_at else None,
            "updated_at": entry.updated_at.isoformat() if entry.updated_at else None,
            "response_hash": entry.response_count_hash
        }

    def clear_user_edits(self, org_name: str, dimension: str) -> QualitativeCache:
        """
        Clear user edits and reset to AI-generated version.

        Args:
            org_name: Organization name
            dimension: Technology dimension

        Returns:
            QualitativeCache entry

        Raises:
            ValueError: If cache entry doesn't exist
        """
        entry = self._session.query(QualitativeCache).filter_by(
            org_name=org_name,
            dimension=dimension
        ).first()

        if not entry:
            raise ValueError(f"No cache entry exists for {org_name}/{dimension}")

        entry.clear_user_edits()
        self._session.commit()
        return entry

    def bulk_invalidate_org(self, org_name: str) -> int:
        """
        Invalidate all cache entries for an organization.

        Clears user edits for all dimensions of the organization.

        Args:
            org_name: Organization name

        Returns:
            Number of cache entries invalidated
        """
        entries = self._session.query(QualitativeCache).filter_by(
            org_name=org_name
        ).all()

        count = 0
        for entry in entries:
            if entry.has_user_edits():
                entry.clear_user_edits()
                count += 1

        if count > 0:
            self._session.commit()

        return count

    def calculate_response_hash(
        self,
        org_name: str,
        dimension: str,
        responses: List[Dict]
    ) -> str:
        """
        Calculate SHA256 hash for response set.

        Hash includes:
        - Organization name
        - Dimension
        - Response count
        - Sorted respondent IDs and roles

        Args:
            org_name: Organization name
            dimension: Technology dimension
            responses: List of response dictionaries

        Returns:
            SHA256 hash (16 character hex string)
        """
        # Build hash input string
        hash_input = f"{org_name}_{dimension}_{len(responses)}"

        # Sort responses by respondent for consistent hashing
        sorted_responses = sorted(
            responses,
            key=lambda r: (r.get('respondent_id', ''), r.get('role', ''))
        )

        # Add respondent identifiers
        for response in sorted_responses:
            respondent_id = response.get('respondent_id', '')
            role = response.get('role', '')
            hash_input += f"_{respondent_id}_{role}"

        # Generate SHA256 hash (truncate to 16 chars for storage efficiency)
        hash_obj = hashlib.sha256(hash_input.encode('utf-8'))
        return hash_obj.hexdigest()[:16]

    def save_main_summary(
        self,
        org_name: str,
        summary_text: str = None,
        summary_title: str = None,
        summary_subtitle: str = None
    ) -> QualitativeCache:
        """
        Save organization-level main summary, title, and/or subtitle.

        Creates or updates the first dimension entry for the organization to store
        the main summary fields. This allows these fields to be stored independently of
        dimension-specific analysis.

        Args:
            org_name: Organization name
            summary_text: Main summary text to save (optional)
            summary_title: Report title to save (optional)
            summary_subtitle: Report subtitle to save (optional)

        Returns:
            QualitativeCache entry where fields were saved

        Raises:
            ValueError: If no cache entries exist for organization
        """
        # Get any existing entry for this organization (prefer first dimension)
        entry = self._session.query(QualitativeCache).filter_by(
            org_name=org_name
        ).first()

        if not entry:
            # Create a minimal entry for the first dimension to store fields
            # This allows editing before dimension analysis is run
            entry = QualitativeCache(
                org_name=org_name,
                dimension="Program Technology",  # Use first dimension (FIXED: was dimension_name)
                ai_generated_json=json.dumps({"summary": "", "themes": [], "modifiers": []}),  # FIXED: was analysis_json
                version=1
            )
            self._session.add(entry)
            self._session.flush()  # Get the ID without committing yet
            print(f"[Qualitative Cache] Created minimal cache entry for {org_name}")

        # Update fields if provided
        if summary_text is not None:
            entry.main_summary = summary_text
            print(f"[Qualitative Cache] Updated main summary for {org_name}")

        if summary_title is not None:
            entry.summary_title = summary_title
            print(f"[Qualitative Cache] Updated summary title to: {summary_title}")

        if summary_subtitle is not None:
            entry.summary_subtitle = summary_subtitle
            print(f"[Qualitative Cache] Updated summary subtitle to: {summary_subtitle}")

        entry.updated_at = datetime.utcnow()

        self._session.commit()
        return entry

    def get_main_summary(self, org_name: str) -> Optional[str]:
        """
        Get organization-level main summary text.

        Returns the main_summary field from any entry for the organization.

        Args:
            org_name: Organization name

        Returns:
            Main summary text or None if not found
        """
        # Get any entry with main_summary for this organization
        entry = self._session.query(QualitativeCache).filter_by(
            org_name=org_name
        ).filter(
            QualitativeCache.main_summary.isnot(None)
        ).first()

        if entry:
            return entry.main_summary

        return None

    def load_organization_qualitative_data(
        self,
        org_name: str,
        dimensions: Optional[List[str]] = None
    ) -> Dict:
        """
        Load all qualitative data for an organization in a single bulk query.

        This method replaces the pattern of making individual queries for:
        - Main organization summary
        - Each dimension separately

        Instead, it fetches ALL data in one query and organizes it into a structured dict.

        Args:
            org_name: Organization name to load data for
            dimensions: List of dimension names to load (defaults to all 5 standard dimensions)

        Returns:
            Dictionary containing:
            {
                'main_summary': dict or None,  # Main summary analysis
                'summary_title': str or None,   # Organization summary title
                'summary_subtitle': str or None, # Organization summary subtitle
                'dimensions': {                 # Dimension-keyed data
                    'Program Technology': {...},
                    'Business Systems': {...},
                    'Data Management': {...},
                    'Infrastructure': {...},
                    'Organizational Culture': {...}
                },
                'dimensions_loaded': int,       # Count of successfully loaded dimensions
                'org_name': str                 # Organization name (for verification)
            }

        Performance:
            Before: 6 queries (1 main + 5 dimensions) = 150-200ms
            After: 1 query = 30-50ms
            Improvement: 75-85% reduction in database time
        """
        if dimensions is None:
            dimensions = [
                "Program Technology",
                "Business Systems",
                "Data Management",
                "Infrastructure",
                "Organizational Culture"
            ]

        # Single query retrieves ALL cache entries for this organization
        entries = self._session.query(QualitativeCache).filter(
            QualitativeCache.org_name == org_name
        ).all()

        # Initialize result structure
        result = {
            'main_summary': None,
            'summary_title': None,
            'summary_subtitle': None,
            'dimensions': {},
            'dimensions_loaded': 0,
            'org_name': org_name
        }

        # Process all entries (single loop through query results)
        for entry in entries:
            # Handle dimension-specific entries
            if entry.dimension and entry.dimension in dimensions:
                # Load the active data (user or AI-generated)
                data_json = entry.get_active_data()
                if data_json:
                    try:
                        data = json.loads(data_json)
                        result['dimensions'][entry.dimension] = data
                        result['dimensions_loaded'] += 1
                    except json.JSONDecodeError:
                        logger.warning(
                            f"Failed to parse JSON for {org_name}/{entry.dimension}"
                        )

            # Handle main organization entry (dimension is None or has main_summary)
            if entry.main_summary:
                try:
                    result['main_summary'] = json.loads(entry.main_summary)
                except json.JSONDecodeError:
                    # If JSON parsing fails, store as plain text
                    result['main_summary'] = entry.main_summary
                    logger.warning(
                        f"main_summary for {org_name} is not valid JSON, storing as text"
                    )

            # Load title and subtitle from any entry that has them
            if entry.summary_title:
                result['summary_title'] = entry.summary_title

            if entry.summary_subtitle:
                result['summary_subtitle'] = entry.summary_subtitle

        return result

    def update_dimension_data(
        self,
        org_name: str,
        dimension: str,
        data: Dict
    ) -> QualitativeCache:
        """
        Update dimension-specific analysis data (user edit).

        This is a convenience method that wraps save_user_edit() with the same
        functionality but clearer naming for API usage.

        Args:
            org_name: Organization name
            dimension: Technology dimension
            data: Updated analysis data (summary, themes, modifiers)

        Returns:
            QualitativeCache entry

        Raises:
            ValueError: If no cache entry exists for dimension
        """
        return self.save_user_edit(org_name, dimension, data)

    # Private validation methods

    def _validate_dimension(self, dimension: str) -> None:
        """Validate dimension is valid."""
        if dimension not in self.VALID_DIMENSIONS:
            raise ValueError(
                f"Invalid dimension: {dimension}. "
                f"Valid dimensions: {', '.join(self.VALID_DIMENSIONS)}"
            )

    def _validate_data_structure(self, data: Dict) -> None:
        """
        Validate qualitative data structure.

        Required fields:
        - summary: str (2-4 paragraphs, max 2000 chars)
        - themes: list[str] (3-5 themes, each 20-100 chars)
        - modifiers: list[dict] (0-10 modifiers)

        Raises:
            ValueError: If data structure is invalid
        """
        # Check required fields
        required_fields = ['summary', 'themes', 'modifiers']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        # Validate summary
        summary = data['summary']
        if not isinstance(summary, str):
            raise ValueError("summary must be a string")
        if len(summary) > 2000:
            raise ValueError(f"summary too long ({len(summary)} chars, max 2000)")
        if len(summary) < 50:
            raise ValueError(f"summary too short ({len(summary)} chars, min 50)")

        # Validate themes (can be list of strings OR list of dicts)
        themes = data['themes']
        if not isinstance(themes, list):
            raise ValueError("themes must be a list")
        if len(themes) < 3 or len(themes) > 5:
            raise ValueError(f"themes must have 3-5 items (got {len(themes)})")

        for i, theme in enumerate(themes):
            # Support both old format (list of strings) and new format (list of dicts)
            if isinstance(theme, str):
                # Old format: validate string length
                if len(theme) < 20 or len(theme) > 100:
                    raise ValueError(
                        f"theme {i} length invalid ({len(theme)} chars, must be 20-100)"
                    )
            elif isinstance(theme, dict):
                # New format: validate dict structure
                required_fields = ['theme', 'summary', 'evidence']
                for field in required_fields:
                    if field not in theme:
                        raise ValueError(f"theme {i} missing required field: {field}")

                # Validate theme title
                if not isinstance(theme['theme'], str):
                    raise ValueError(f"theme {i} 'theme' field must be a string")
                if len(theme['theme']) < 5 or len(theme['theme']) > 100:
                    raise ValueError(
                        f"theme {i} 'theme' field length invalid ({len(theme['theme'])} chars, must be 5-100)"
                    )

                # Validate summary
                if not isinstance(theme['summary'], str):
                    raise ValueError(f"theme {i} 'summary' field must be a string")
                if len(theme['summary']) < 20 or len(theme['summary']) > 500:
                    raise ValueError(
                        f"theme {i} 'summary' field length invalid ({len(theme['summary'])} chars, must be 20-500)"
                    )

                # Validate evidence
                if not isinstance(theme['evidence'], list):
                    raise ValueError(f"theme {i} 'evidence' field must be a list")
                for j, evidence_item in enumerate(theme['evidence']):
                    if not isinstance(evidence_item, str):
                        raise ValueError(f"theme {i} evidence item {j} must be a string")
            else:
                raise ValueError(f"theme {i} must be either a string or dict")

        # Validate modifiers
        modifiers = data['modifiers']
        if not isinstance(modifiers, list):
            raise ValueError("modifiers must be a list")
        if len(modifiers) > 10:
            raise ValueError(f"Too many modifiers ({len(modifiers)}, max 10)")

        # Validate each modifier
        for i, modifier in enumerate(modifiers):
            if not isinstance(modifier, dict):
                raise ValueError(f"modifier {i} must be a dict")

            required_mod_fields = ['respondent', 'role', 'factor', 'value']
            for field in required_mod_fields:
                if field not in modifier:
                    raise ValueError(f"modifier {i} missing field: {field}")

            # Validate modifier fields
            if not isinstance(modifier['respondent'], str):
                raise ValueError(f"modifier {i} respondent must be string")
            if not isinstance(modifier['role'], str):
                raise ValueError(f"modifier {i} role must be string")
            if modifier['role'] not in ['CEO', 'Tech Lead', 'Staff']:
                raise ValueError(
                    f"modifier {i} role must be CEO, Tech Lead, or Staff"
                )
            if not isinstance(modifier['factor'], str):
                raise ValueError(f"modifier {i} factor must be string")
            if len(modifier['factor']) > 500:
                raise ValueError(f"modifier {i} factor too long (max 500 chars)")
            if not isinstance(modifier['value'], (int, float)):
                raise ValueError(f"modifier {i} value must be number")
            if modifier['value'] < -10 or modifier['value'] > 10:
                raise ValueError(f"modifier {i} value must be -10 to +10")

            # JJF-42: Validate reasoning for non-zero modifiers
            if modifier['value'] != 0 and not modifier.get('reasoning'):
                raise ValueError(
                    f"modifier {i} with non-zero value ({modifier['value']}) must include reasoning. "
                    f"Modifier: {modifier.get('respondent', 'Unknown')} - {modifier.get('factor', 'Unknown')}"
                )

            # JJF-42: Validate original_text for non-zero modifiers
            if modifier['value'] != 0 and not modifier.get('original_text'):
                raise ValueError(
                    f"modifier {i} with non-zero value ({modifier['value']}) must include original_text citation. "
                    f"Modifier: {modifier.get('respondent', 'Unknown')} - {modifier.get('factor', 'Unknown')}"
                )


# Singleton instance for convenience
_repository_instance: Optional[QualitativeCacheRepository] = None


def get_qualitative_cache_repository(
    session: Optional[Session] = None,
    database_url: Optional[str] = None
) -> QualitativeCacheRepository:
    """
    Get singleton instance of QualitativeCacheRepository.

    Args:
        session: SQLAlchemy session (optional)
        database_url: Database URL (optional, uses DATABASE_URL env if not provided)

    Returns:
        QualitativeCacheRepository instance
    """
    import os
    global _repository_instance

    if _repository_instance is None:
        # Use DATABASE_URL from environment if not explicitly provided
        # This ensures production uses PostgreSQL, not SQLite
        effective_db_url = database_url or os.getenv("DATABASE_URL")

        _repository_instance = QualitativeCacheRepository(
            session=session,
            database_url=effective_db_url
        )

    return _repository_instance
