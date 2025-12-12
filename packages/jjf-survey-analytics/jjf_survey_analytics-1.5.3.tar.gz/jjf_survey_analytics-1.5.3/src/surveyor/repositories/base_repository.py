"""
Base repository pattern implementation.
"""

import logging
from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models.base import BaseModel

T = TypeVar("T", bound=BaseModel)

logger = logging.getLogger(__name__)


class IRepository(ABC, Generic[T]):
    """Interface for repository pattern."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """Get entity by ID."""

    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities."""

    @abstractmethod
    def create(self, entity: T) -> T:
        """Create new entity."""

    @abstractmethod
    def update(self, entity: T) -> T:
        """Update existing entity."""

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Delete entity by ID."""


class BaseRepository(IRepository[T]):
    """Base repository implementation."""

    def __init__(self, session: Session, model_class: Type[T]):
        self.session = session
        self.model_class = model_class

    def get_by_id(self, id: int) -> Optional[T]:
        """Get entity by ID."""
        try:
            return self.session.query(self.model_class).filter(self.model_class.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting {self.model_class.__name__} by ID {id}: {e}")
            raise

    def get_all(self) -> List[T]:
        """Get all entities."""
        try:
            return self.session.query(self.model_class).all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting all {self.model_class.__name__}: {e}")
            raise

    def create(self, entity: T) -> T:
        """Create new entity."""
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating {self.model_class.__name__}: {e}")
            raise

    def update(self, entity: T) -> T:
        """Update existing entity."""
        try:
            self.session.merge(entity)
            self.session.commit()
            return entity
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating {self.model_class.__name__}: {e}")
            raise

    def delete(self, id: int) -> bool:
        """Delete entity by ID."""
        try:
            entity = self.get_by_id(id)
            if entity:
                self.session.delete(entity)
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting {self.model_class.__name__} with ID {id}: {e}")
            raise

    def find_by(self, **kwargs) -> List[T]:
        """Find entities by criteria."""
        try:
            query = self.session.query(self.model_class)
            for key, value in kwargs.items():
                if hasattr(self.model_class, key):
                    query = query.filter(getattr(self.model_class, key) == value)
            return query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error finding {self.model_class.__name__} by criteria {kwargs}: {e}")
            raise

    def find_one_by(self, **kwargs) -> Optional[T]:
        """Find one entity by criteria."""
        results = self.find_by(**kwargs)
        return results[0] if results else None
