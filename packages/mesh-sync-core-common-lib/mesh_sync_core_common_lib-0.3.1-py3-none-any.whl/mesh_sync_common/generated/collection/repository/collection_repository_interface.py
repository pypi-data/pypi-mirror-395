# AUTO-GENERATED - DO NOT EDIT
# Generated from: collection/domain/collection.agg.yaml
"""
Repository interface for Collection aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.collection.collection import Collection
from mesh_sync_common.generated.collection.thumbnail_type_base import ThumbnailType
from mesh_sync_common.generated.collection.thumbnail_status_base import ThumbnailStatus


__all__ = [
    'CollectionFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'ICollectionRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class CollectionFilterCriteria:
    """Filter criteria for querying Collection entities"""
    user_id: Optional[UUID] = None
    thumbnail_type: Optional[ThumbnailType] = None
    thumbnail_status: Optional[ThumbnailStatus] = None
    thumbnail_source_connection_id: Optional[UUID] = None


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


class ICollectionRepository(ABC):
    """
    Repository interface for Collection aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[Collection]:
        """
        Find a Collection by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The Collection or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[CollectionFilterCriteria] = None
    ) -> List[Collection]:
        """
        Find all Collection entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching Collection entities
        """
        pass

    @abstractmethod
    async def save(self, collection: Collection) -> Collection:
        """
        Save a Collection (create or update)
        
        Args:
            collection: The Collection to save
            
        Returns:
            The saved Collection
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a Collection by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a Collection exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[CollectionFilterCriteria] = None
    ) -> int:
        """
        Count Collection entities matching the given criteria
        
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
        criteria: Optional[CollectionFilterCriteria] = None
    ) -> PaginatedResult[Collection]:
        """
        Find Collection entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
