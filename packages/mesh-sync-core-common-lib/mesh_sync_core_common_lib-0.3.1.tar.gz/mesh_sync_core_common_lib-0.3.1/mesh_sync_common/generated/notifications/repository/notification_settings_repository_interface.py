# AUTO-GENERATED - DO NOT EDIT
# Generated from: notifications/domain/notification_settings.agg.yaml
"""
Repository interface for NotificationSettings aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.notifications.notification_settings import NotificationSettings
from mesh_sync_common.generated.notifications.notification_frequency_base import NotificationFrequency


__all__ = [
    'NotificationSettingsFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'INotificationSettingsRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class NotificationSettingsFilterCriteria:
    """Filter criteria for querying NotificationSettings entities"""
    user_id: Optional[UUID] = None
    frequency: Optional[NotificationFrequency] = None


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


class INotificationSettingsRepository(ABC):
    """
    Repository interface for NotificationSettings aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[NotificationSettings]:
        """
        Find a NotificationSettings by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The NotificationSettings or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[NotificationSettingsFilterCriteria] = None
    ) -> List[NotificationSettings]:
        """
        Find all NotificationSettings entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching NotificationSettings entities
        """
        pass

    @abstractmethod
    async def save(self, notification_settings: NotificationSettings) -> NotificationSettings:
        """
        Save a NotificationSettings (create or update)
        
        Args:
            notification_settings: The NotificationSettings to save
            
        Returns:
            The saved NotificationSettings
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a NotificationSettings by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a NotificationSettings exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[NotificationSettingsFilterCriteria] = None
    ) -> int:
        """
        Count NotificationSettings entities matching the given criteria
        
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
        criteria: Optional[NotificationSettingsFilterCriteria] = None
    ) -> PaginatedResult[NotificationSettings]:
        """
        Find NotificationSettings entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
