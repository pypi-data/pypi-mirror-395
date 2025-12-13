# AUTO-GENERATED - DO NOT EDIT
# Generated from: metamodel/domain/metamodel_rating.agg.yaml
"""
Repository interface for MetamodelRating aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.metamodel.metamodel_rating import MetamodelRating


__all__ = [
    'MetamodelRatingFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'IMetamodelRatingRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class MetamodelRatingFilterCriteria:
    """Filter criteria for querying MetamodelRating entities"""
    user_id: Optional[UUID] = None
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


class IMetamodelRatingRepository(ABC):
    """
    Repository interface for MetamodelRating aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[MetamodelRating]:
        """
        Find a MetamodelRating by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The MetamodelRating or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[MetamodelRatingFilterCriteria] = None
    ) -> List[MetamodelRating]:
        """
        Find all MetamodelRating entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching MetamodelRating entities
        """
        pass

    @abstractmethod
    async def save(self, metamodel_rating: MetamodelRating) -> MetamodelRating:
        """
        Save a MetamodelRating (create or update)
        
        Args:
            metamodel_rating: The MetamodelRating to save
            
        Returns:
            The saved MetamodelRating
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a MetamodelRating by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a MetamodelRating exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[MetamodelRatingFilterCriteria] = None
    ) -> int:
        """
        Count MetamodelRating entities matching the given criteria
        
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
        criteria: Optional[MetamodelRatingFilterCriteria] = None
    ) -> PaginatedResult[MetamodelRating]:
        """
        Find MetamodelRating entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
