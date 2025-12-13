# AUTO-GENERATED - DO NOT EDIT
# Generated from: storage/domain/storage_provider_config.agg.yaml
"""
Repository interface for StorageProviderConfig aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.storage.storage_provider_config import StorageProviderConfig
from mesh_sync_common.generated.storage.storage_provider_type_base import StorageProviderType


__all__ = [
    'StorageProviderConfigFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'IStorageProviderConfigRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class StorageProviderConfigFilterCriteria:
    """Filter criteria for querying StorageProviderConfig entities"""
    user_id: Optional[UUID] = None
    type: Optional[StorageProviderType] = None


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


class IStorageProviderConfigRepository(ABC):
    """
    Repository interface for StorageProviderConfig aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[StorageProviderConfig]:
        """
        Find a StorageProviderConfig by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The StorageProviderConfig or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[StorageProviderConfigFilterCriteria] = None
    ) -> List[StorageProviderConfig]:
        """
        Find all StorageProviderConfig entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching StorageProviderConfig entities
        """
        pass

    @abstractmethod
    async def save(self, storage_provider_config: StorageProviderConfig) -> StorageProviderConfig:
        """
        Save a StorageProviderConfig (create or update)
        
        Args:
            storage_provider_config: The StorageProviderConfig to save
            
        Returns:
            The saved StorageProviderConfig
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a StorageProviderConfig by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a StorageProviderConfig exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[StorageProviderConfigFilterCriteria] = None
    ) -> int:
        """
        Count StorageProviderConfig entities matching the given criteria
        
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
        criteria: Optional[StorageProviderConfigFilterCriteria] = None
    ) -> PaginatedResult[StorageProviderConfig]:
        """
        Find StorageProviderConfig entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
