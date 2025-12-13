# AUTO-GENERATED - DO NOT EDIT
# Generated from: tag/domain/tag.agg.yaml
"""
Repository interface for Tag aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.tag.tag import Tag


__all__ = [
    'TagFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'ITagRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class TagFilterCriteria:
    """Filter criteria for querying Tag entities"""
    user_id: Optional[UUID] = None


@dataclass
class PaginationOptions:
    """Pagination options"""
    page: int = 1
    limit: int = 20
    sort_by: Optional[str] = None
    sort_order: str = 'ASC'


@dataclass
class PaginatedResult(Generic[T]):
    """Paginated result"""
    items: List[T]
    total: int
    page: int
    limit: int

    @property
    def total_pages(self) -> int:
        return (self.total + self.limit - 1) // self.limit


class ITagRepository(ABC):
    """
    Repository interface for Tag aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[Tag]:
        """
        Find a Tag by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The Tag or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[TagFilterCriteria] = None
    ) -> List[Tag]:
        """
        Find all Tag entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching Tag entities
        """
        pass

    @abstractmethod
    async def save(self, tag: Tag) -> Tag:
        """
        Save a Tag (create or update)
        
        Args:
            tag: The Tag to save
            
        Returns:
            The saved Tag
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a Tag by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a Tag exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[TagFilterCriteria] = None
    ) -> int:
        """
        Count Tag entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            The count
        """
        pass

    @abstractmethod
    async def find_paginated(
        self,
        options: PaginationOptions,
        criteria: Optional[TagFilterCriteria] = None
    ) -> PaginatedResult[Tag]:
        """
        Find Tag entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
