# AUTO-GENERATED - DO NOT EDIT
# Generated from: media/domain/thumbnail_media.agg.yaml
"""
Repository interface for ThumbnailMedia aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.media.thumbnail_media import ThumbnailMedia
from mesh_sync_common.generated.media.media_type_base import MediaType


__all__ = [
    'ThumbnailMediaFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'IThumbnailMediaRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class ThumbnailMediaFilterCriteria:
    """Filter criteria for querying ThumbnailMedia entities"""
    media_type: Optional[MediaType] = None


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


class IThumbnailMediaRepository(ABC):
    """
    Repository interface for ThumbnailMedia aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[ThumbnailMedia]:
        """
        Find a ThumbnailMedia by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The ThumbnailMedia or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[ThumbnailMediaFilterCriteria] = None
    ) -> List[ThumbnailMedia]:
        """
        Find all ThumbnailMedia entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching ThumbnailMedia entities
        """
        pass

    @abstractmethod
    async def save(self, thumbnail_media: ThumbnailMedia) -> ThumbnailMedia:
        """
        Save a ThumbnailMedia (create or update)
        
        Args:
            thumbnail_media: The ThumbnailMedia to save
            
        Returns:
            The saved ThumbnailMedia
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a ThumbnailMedia by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a ThumbnailMedia exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[ThumbnailMediaFilterCriteria] = None
    ) -> int:
        """
        Count ThumbnailMedia entities matching the given criteria
        
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
        criteria: Optional[ThumbnailMediaFilterCriteria] = None
    ) -> PaginatedResult[ThumbnailMedia]:
        """
        Find ThumbnailMedia entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
