# AUTO-GENERATED - DO NOT EDIT
# Generated from: texture/domain/texture.agg.yaml
"""
Repository interface for Texture aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.texture.texture import Texture
from mesh_sync_common.generated.texture.texture_type_base import TextureType


__all__ = [
    'TextureFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'ITextureRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class TextureFilterCriteria:
    """Filter criteria for querying Texture entities"""
    user_id: Optional[UUID] = None
    type: Optional[TextureType] = None
    storage_item_id: Optional[UUID] = None


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


class ITextureRepository(ABC):
    """
    Repository interface for Texture aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[Texture]:
        """
        Find a Texture by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The Texture or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[TextureFilterCriteria] = None
    ) -> List[Texture]:
        """
        Find all Texture entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching Texture entities
        """
        pass

    @abstractmethod
    async def save(self, texture: Texture) -> Texture:
        """
        Save a Texture (create or update)
        
        Args:
            texture: The Texture to save
            
        Returns:
            The saved Texture
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a Texture by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a Texture exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[TextureFilterCriteria] = None
    ) -> int:
        """
        Count Texture entities matching the given criteria
        
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
        criteria: Optional[TextureFilterCriteria] = None
    ) -> PaginatedResult[Texture]:
        """
        Find Texture entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
