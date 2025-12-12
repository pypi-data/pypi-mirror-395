"""
Base model classes and database setup.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class BaseModel(Base):
    """Base model with common fields."""

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


def create_database_engine(database_url: str, echo: bool = False):
    """Create database engine."""
    return create_engine(database_url, echo=echo)


def create_session_factory(engine):
    """Create session factory."""
    return sessionmaker(bind=engine)


def create_tables(engine):
    """Create all tables."""
    Base.metadata.create_all(engine)
