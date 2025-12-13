# AUTO-GENERATED - DO NOT EDIT
# Generated from: marketplace/domain/marketplace_item.agg.yaml
"""
Repository interface for MarketplaceItem aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.marketplace.marketplace_item import MarketplaceItem
from mesh_sync_common.generated.marketplace.marketplace_item_status_base import MarketplaceItemStatus


__all__ = [
    'MarketplaceItemFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'IMarketplaceItemRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class MarketplaceItemFilterCriteria:
    """Filter criteria for querying MarketplaceItem entities"""
    model_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    status: Optional[MarketplaceItemStatus] = None


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


class IMarketplaceItemRepository(ABC):
    """
    Repository interface for MarketplaceItem aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[MarketplaceItem]:
        """
        Find a MarketplaceItem by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The MarketplaceItem or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[MarketplaceItemFilterCriteria] = None
    ) -> List[MarketplaceItem]:
        """
        Find all MarketplaceItem entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching MarketplaceItem entities
        """
        pass

    @abstractmethod
    async def save(self, marketplace_item: MarketplaceItem) -> MarketplaceItem:
        """
        Save a MarketplaceItem (create or update)
        
        Args:
            marketplace_item: The MarketplaceItem to save
            
        Returns:
            The saved MarketplaceItem
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a MarketplaceItem by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a MarketplaceItem exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[MarketplaceItemFilterCriteria] = None
    ) -> int:
        """
        Count MarketplaceItem entities matching the given criteria
        
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
        criteria: Optional[MarketplaceItemFilterCriteria] = None
    ) -> PaginatedResult[MarketplaceItem]:
        """
        Find MarketplaceItem entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
