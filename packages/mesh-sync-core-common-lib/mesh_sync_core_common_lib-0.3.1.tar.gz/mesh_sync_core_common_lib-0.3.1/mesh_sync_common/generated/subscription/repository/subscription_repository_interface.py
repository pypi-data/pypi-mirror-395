# AUTO-GENERATED - DO NOT EDIT
# Generated from: subscription/domain/subscription.agg.yaml
"""
Repository interface for Subscription aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.subscription.subscription import Subscription
from mesh_sync_common.generated.subscription.plan_tier_base import PlanTier
from mesh_sync_common.generated.subscription.subscription_status_base import SubscriptionStatus


__all__ = [
    'SubscriptionFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'ISubscriptionRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class SubscriptionFilterCriteria:
    """Filter criteria for querying Subscription entities"""
    user_id: Optional[UUID] = None
    plan_id: Optional[PlanTier] = None
    status: Optional[SubscriptionStatus] = None


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


class ISubscriptionRepository(ABC):
    """
    Repository interface for Subscription aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[Subscription]:
        """
        Find a Subscription by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The Subscription or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[SubscriptionFilterCriteria] = None
    ) -> List[Subscription]:
        """
        Find all Subscription entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching Subscription entities
        """
        pass

    @abstractmethod
    async def save(self, subscription: Subscription) -> Subscription:
        """
        Save a Subscription (create or update)
        
        Args:
            subscription: The Subscription to save
            
        Returns:
            The saved Subscription
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a Subscription by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a Subscription exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[SubscriptionFilterCriteria] = None
    ) -> int:
        """
        Count Subscription entities matching the given criteria
        
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
        criteria: Optional[SubscriptionFilterCriteria] = None
    ) -> PaginatedResult[Subscription]:
        """
        Find Subscription entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
