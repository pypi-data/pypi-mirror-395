# AUTO-GENERATED - DO NOT EDIT
# Generated from: library/domain/library.agg.yaml
"""
Repository interface for Library aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.library.library import Library
from mesh_sync_common.generated.library.library_scan_status_base import LibraryScanStatus


__all__ = [
    'LibraryFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'ILibraryRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class LibraryFilterCriteria:
    """Filter criteria for querying Library entities"""
    scan_status: Optional[LibraryScanStatus] = None
    storage_provider_config_id: Optional[UUID] = None
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


class ILibraryRepository(ABC):
    """
    Repository interface for Library aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[Library]:
        """
        Find a Library by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The Library or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[LibraryFilterCriteria] = None
    ) -> List[Library]:
        """
        Find all Library entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching Library entities
        """
        pass

    @abstractmethod
    async def save(self, library: Library) -> Library:
        """
        Save a Library (create or update)
        
        Args:
            library: The Library to save
            
        Returns:
            The saved Library
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a Library by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a Library exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[LibraryFilterCriteria] = None
    ) -> int:
        """
        Count Library entities matching the given criteria
        
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
        criteria: Optional[LibraryFilterCriteria] = None
    ) -> PaginatedResult[Library]:
        """
        Find Library entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
