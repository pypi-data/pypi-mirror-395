# AUTO-GENERATED - DO NOT EDIT
# Generated from: catalog/domain/model.agg.yaml
"""
Repository interface for Model aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.catalog.model import Model
from mesh_sync_common.generated.catalog.model_status_base import ModelStatus


__all__ = [
    'ModelFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'IModelRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class ModelFilterCriteria:
    """Filter criteria for querying Model entities"""
    status: Optional[ModelStatus] = None
    owner_id: Optional[UUID] = None
    library_id: Optional[UUID] = None


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


class IModelRepository(ABC):
    """
    Repository interface for Model aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[Model]:
        """
        Find a Model by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The Model or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[ModelFilterCriteria] = None
    ) -> List[Model]:
        """
        Find all Model entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching Model entities
        """
        pass

    @abstractmethod
    async def save(self, model: Model) -> Model:
        """
        Save a Model (create or update)
        
        Args:
            model: The Model to save
            
        Returns:
            The saved Model
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a Model by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a Model exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[ModelFilterCriteria] = None
    ) -> int:
        """
        Count Model entities matching the given criteria
        
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
        criteria: Optional[ModelFilterCriteria] = None
    ) -> PaginatedResult[Model]:
        """
        Find Model entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
