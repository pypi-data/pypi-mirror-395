# AUTO-GENERATED - DO NOT EDIT
# Generated from: marketplace/domain/marketplace_listing.agg.yaml
"""
Repository interface for MarketplaceListing aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.marketplace.marketplace_listing import MarketplaceListing
from mesh_sync_common.generated.marketplace.marketplace_listing_status_base import MarketplaceListingStatus


__all__ = [
    'MarketplaceListingFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'IMarketplaceListingRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class MarketplaceListingFilterCriteria:
    """Filter criteria for querying MarketplaceListing entities"""
    model_id: Optional[UUID] = None
    status: Optional[MarketplaceListingStatus] = None


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


class IMarketplaceListingRepository(ABC):
    """
    Repository interface for MarketplaceListing aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[MarketplaceListing]:
        """
        Find a MarketplaceListing by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The MarketplaceListing or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[MarketplaceListingFilterCriteria] = None
    ) -> List[MarketplaceListing]:
        """
        Find all MarketplaceListing entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching MarketplaceListing entities
        """
        pass

    @abstractmethod
    async def save(self, marketplace_listing: MarketplaceListing) -> MarketplaceListing:
        """
        Save a MarketplaceListing (create or update)
        
        Args:
            marketplace_listing: The MarketplaceListing to save
            
        Returns:
            The saved MarketplaceListing
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a MarketplaceListing by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a MarketplaceListing exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[MarketplaceListingFilterCriteria] = None
    ) -> int:
        """
        Count MarketplaceListing entities matching the given criteria
        
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
        criteria: Optional[MarketplaceListingFilterCriteria] = None
    ) -> PaginatedResult[MarketplaceListing]:
        """
        Find MarketplaceListing entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
