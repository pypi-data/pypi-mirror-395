"""
SQLAlchemy model for report_qualitative_cache table.

This table stores AI-generated and user-edited qualitative analysis data
for organization assessment reports across five technology dimensions.

JSON Schema for ai_generated_json and user_edited_json:
-------------------------------------------------------
{
    "summary": str,              # 2-4 paragraph qualitative summary
    "themes": [str, str, ...],   # 3-5 key themes identified
    "modifiers": [               # Score adjustment factors
        {
            "respondent": str,   # Respondent identifier
            "role": str,         # Role (CEO, Tech Lead, Staff)
            "factor": str,       # Reason for modifier
            "value": int         # Adjustment (-10 to +10)
        }
    ]
}

Cache Invalidation Strategy:
----------------------------
- response_count_hash: SHA256 hash of (org_name + dimension + response_count + respondent_ids)
- When hash changes (new/removed responses), cache is invalidated
- User edits preserved until underlying data changes
- Version increments on each user edit

Usage Example:
-------------
from src.surveyor.models.qualitative_cache import QualitativeCache
from src.surveyor.models.base import create_database_engine, create_session_factory

# Create engine and session
engine = create_database_engine("sqlite:///survey.db")
Session = create_session_factory(engine)
session = Session()

# Create entry
cache_entry = QualitativeCache(
    org_name="Example Org",
    dimension="Program Technology",
    ai_generated_json='{"summary": "...", "themes": [...], "modifiers": [...]}',
    response_count_hash="abc123..."
)
session.add(cache_entry)
session.commit()

# Query entry
entry = session.query(QualitativeCache).filter_by(
    org_name="Example Org",
    dimension="Program Technology"
).first()
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Index, Integer, String, Text

from .base import BaseModel


class QualitativeCache(BaseModel):
    """
    Stores cached qualitative analysis data for organization reports.

    Supports both AI-generated initial analysis and user edits with
    cache invalidation based on underlying response data changes.
    """

    __tablename__ = "report_qualitative_cache"

    # Organization and dimension identifiers
    org_name = Column(String(255), nullable=False, comment="Organization name")
    dimension = Column(
        String(100),
        nullable=False,
        comment="Technology dimension (Program Technology, Business Systems, etc.)"
    )

    # AI-generated analysis data
    ai_generated_json = Column(
        Text,
        nullable=False,
        comment="AI-generated qualitative analysis (JSON blob)"
    )

    # User-edited analysis data (optional)
    user_edited_json = Column(
        Text,
        nullable=True,
        comment="User-edited qualitative analysis (JSON blob, NULL if not edited)"
    )

    # Organization-level main summary (optional)
    main_summary = Column(
        Text,
        nullable=True,
        comment="Organization-level main summary text (editable independently)"
    )

    # Organization summary title and subtitle
    summary_title = Column(
        Text,
        nullable=True,
        comment="Organization report title (editable, defaults to 'Technology Maturity Assessment Report')"
    )

    summary_subtitle = Column(
        Text,
        nullable=True,
        comment="Organization report subtitle (editable, defaults to 'Technology Assessment Overview')"
    )

    # Version tracking
    version = Column(
        Integer,
        default=1,
        nullable=False,
        comment="Increments on each user edit (starts at 1)"
    )

    # Cache invalidation hash
    response_count_hash = Column(
        String(64),
        nullable=True,
        comment="SHA256 hash for cache invalidation (org+dimension+response_count)"
    )

    # Timestamps are inherited from BaseModel (created_at, updated_at)
    # Note: updated_at auto-updates on any modification via BaseModel.onupdate

    # Unique constraint on (org_name, dimension) - only one cache entry per org/dimension
    __table_args__ = (
        Index('idx_qualitative_org_dimension', 'org_name', 'dimension', unique=True),
        Index('idx_qualitative_updated', 'updated_at'),
    )

    def __repr__(self):
        """String representation of cache entry."""
        source = "edited" if self.user_edited_json else "ai"
        return (
            f"<QualitativeCache(org='{self.org_name}', "
            f"dimension='{self.dimension}', version={self.version}, source={source})>"
        )

    def get_active_data(self) -> str:
        """
        Get the active JSON data (user-edited if available, otherwise AI-generated).

        Returns:
            str: JSON string of active analysis data
        """
        return self.user_edited_json if self.user_edited_json else self.ai_generated_json

    def has_user_edits(self) -> bool:
        """
        Check if this cache entry has user edits.

        Returns:
            bool: True if user has edited this entry
        """
        return self.user_edited_json is not None

    def clear_user_edits(self) -> None:
        """
        Clear user edits (revert to AI-generated version).

        This is typically called when underlying response data changes,
        invalidating user edits.
        """
        self.user_edited_json = None
        self.version = 1
        self.updated_at = datetime.utcnow()
