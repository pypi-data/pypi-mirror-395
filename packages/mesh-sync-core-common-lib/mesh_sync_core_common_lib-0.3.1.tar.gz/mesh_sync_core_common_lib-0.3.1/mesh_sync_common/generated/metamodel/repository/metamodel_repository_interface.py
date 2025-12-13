# AUTO-GENERATED - DO NOT EDIT
# Generated from: metamodel/domain/metamodel.agg.yaml
"""
Repository interface for Metamodel aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.metamodel.metamodel import Metamodel
from mesh_sync_common.generated.metamodel.metamodel_status_base import MetamodelStatus


__all__ = [
    'MetamodelFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'IMetamodelRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class MetamodelFilterCriteria:
    """Filter criteria for querying Metamodel entities"""
    owner_id: Optional[UUID] = None
    library_id: Optional[UUID] = None
    status: Optional[MetamodelStatus] = None
    associated_media_id: Optional[UUID] = None
    parent_metamodel_id: Optional[UUID] = None


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


class IMetamodelRepository(ABC):
    """
    Repository interface for Metamodel aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[Metamodel]:
        """
        Find a Metamodel by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The Metamodel or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[MetamodelFilterCriteria] = None
    ) -> List[Metamodel]:
        """
        Find all Metamodel entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching Metamodel entities
        """
        pass

    @abstractmethod
    async def save(self, metamodel: Metamodel) -> Metamodel:
        """
        Save a Metamodel (create or update)
        
        Args:
            metamodel: The Metamodel to save
            
        Returns:
            The saved Metamodel
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a Metamodel by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a Metamodel exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[MetamodelFilterCriteria] = None
    ) -> int:
        """
        Count Metamodel entities matching the given criteria
        
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
        criteria: Optional[MetamodelFilterCriteria] = None
    ) -> PaginatedResult[Metamodel]:
        """
        Find Metamodel entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
