# AUTO-GENERATED - DO NOT EDIT
# Generated from: user/domain/user.agg.yaml
"""
Repository interface for User aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.user.user import User
from mesh_sync_common.generated.user.user_role_base import UserRole


__all__ = [
    'UserFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'IUserRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class UserFilterCriteria:
    """Filter criteria for querying User entities"""
    role: Optional[UserRole] = None


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


class IUserRepository(ABC):
    """
    Repository interface for User aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[User]:
        """
        Find a User by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The User or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[UserFilterCriteria] = None
    ) -> List[User]:
        """
        Find all User entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching User entities
        """
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        """
        Save a User (create or update)
        
        Args:
            user: The User to save
            
        Returns:
            The saved User
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a User by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a User exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[UserFilterCriteria] = None
    ) -> int:
        """
        Count User entities matching the given criteria
        
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
        criteria: Optional[UserFilterCriteria] = None
    ) -> PaginatedResult[User]:
        """
        Find User entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
