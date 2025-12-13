# AUTO-GENERATED - DO NOT EDIT
# Generated from: storage/domain/storage_connection.agg.yaml
"""
Repository interface for StorageConnection aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.storage.storage_connection import StorageConnection
from mesh_sync_common.generated.storage.storage_provider_type_base import StorageProviderType
from mesh_sync_common.generated.storage.scan_status_base import ScanStatus


__all__ = [
    'StorageConnectionFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'IStorageConnectionRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class StorageConnectionFilterCriteria:
    """Filter criteria for querying StorageConnection entities"""
    storage_provider_config_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    library_id: Optional[UUID] = None
    provider_type: Optional[StorageProviderType] = None
    last_scan_status: Optional[ScanStatus] = None


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


class IStorageConnectionRepository(ABC):
    """
    Repository interface for StorageConnection aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[StorageConnection]:
        """
        Find a StorageConnection by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The StorageConnection or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[StorageConnectionFilterCriteria] = None
    ) -> List[StorageConnection]:
        """
        Find all StorageConnection entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching StorageConnection entities
        """
        pass

    @abstractmethod
    async def save(self, storage_connection: StorageConnection) -> StorageConnection:
        """
        Save a StorageConnection (create or update)
        
        Args:
            storage_connection: The StorageConnection to save
            
        Returns:
            The saved StorageConnection
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a StorageConnection by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a StorageConnection exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[StorageConnectionFilterCriteria] = None
    ) -> int:
        """
        Count StorageConnection entities matching the given criteria
        
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
        criteria: Optional[StorageConnectionFilterCriteria] = None
    ) -> PaginatedResult[StorageConnection]:
        """
        Find StorageConnection entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
