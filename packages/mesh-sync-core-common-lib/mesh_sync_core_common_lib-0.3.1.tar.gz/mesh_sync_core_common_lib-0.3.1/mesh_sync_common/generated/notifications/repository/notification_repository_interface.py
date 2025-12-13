# AUTO-GENERATED - DO NOT EDIT
# Generated from: notifications/domain/notification.agg.yaml
"""
Repository interface for Notification aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.notifications.notification import Notification
from mesh_sync_common.generated.notifications.notification_type_base import NotificationType
from mesh_sync_common.generated.notifications.notification_priority_base import NotificationPriority


__all__ = [
    'NotificationFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'INotificationRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class NotificationFilterCriteria:
    """Filter criteria for querying Notification entities"""
    user_id: Optional[UUID] = None
    type: Optional[NotificationType] = None
    priority: Optional[NotificationPriority] = None


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


class INotificationRepository(ABC):
    """
    Repository interface for Notification aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[Notification]:
        """
        Find a Notification by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The Notification or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[NotificationFilterCriteria] = None
    ) -> List[Notification]:
        """
        Find all Notification entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching Notification entities
        """
        pass

    @abstractmethod
    async def save(self, notification: Notification) -> Notification:
        """
        Save a Notification (create or update)
        
        Args:
            notification: The Notification to save
            
        Returns:
            The saved Notification
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a Notification by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a Notification exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[NotificationFilterCriteria] = None
    ) -> int:
        """
        Count Notification entities matching the given criteria
        
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
        criteria: Optional[NotificationFilterCriteria] = None
    ) -> PaginatedResult[Notification]:
        """
        Find Notification entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
