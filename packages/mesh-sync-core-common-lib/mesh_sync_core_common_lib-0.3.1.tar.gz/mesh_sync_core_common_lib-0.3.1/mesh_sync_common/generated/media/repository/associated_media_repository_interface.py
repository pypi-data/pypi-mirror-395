# AUTO-GENERATED - DO NOT EDIT
# Generated from: media/domain/associated_media.agg.yaml
"""
Repository interface for AssociatedMedia aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.media.associated_media import AssociatedMedia


__all__ = [
    'AssociatedMediaFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'IAssociatedMediaRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class AssociatedMediaFilterCriteria:
    """Filter criteria for querying AssociatedMedia entities"""
    model_id: Optional[UUID] = None
    metamodel_id: Optional[UUID] = None


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


class IAssociatedMediaRepository(ABC):
    """
    Repository interface for AssociatedMedia aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[AssociatedMedia]:
        """
        Find a AssociatedMedia by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The AssociatedMedia or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[AssociatedMediaFilterCriteria] = None
    ) -> List[AssociatedMedia]:
        """
        Find all AssociatedMedia entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching AssociatedMedia entities
        """
        pass

    @abstractmethod
    async def save(self, associated_media: AssociatedMedia) -> AssociatedMedia:
        """
        Save a AssociatedMedia (create or update)
        
        Args:
            associated_media: The AssociatedMedia to save
            
        Returns:
            The saved AssociatedMedia
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a AssociatedMedia by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a AssociatedMedia exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[AssociatedMediaFilterCriteria] = None
    ) -> int:
        """
        Count AssociatedMedia entities matching the given criteria
        
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
        criteria: Optional[AssociatedMediaFilterCriteria] = None
    ) -> PaginatedResult[AssociatedMedia]:
        """
        Find AssociatedMedia entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
