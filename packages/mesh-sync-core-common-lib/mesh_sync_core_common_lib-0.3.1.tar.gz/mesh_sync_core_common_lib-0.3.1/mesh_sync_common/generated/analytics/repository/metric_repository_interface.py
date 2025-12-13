# AUTO-GENERATED - DO NOT EDIT
# Generated from: analytics/domain/metric.agg.yaml
"""
Repository interface for Metric aggregate
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from mesh_sync_common.domain.analytics.metric import Metric
from mesh_sync_common.generated.analytics.metric_type_base import MetricType


__all__ = [
    'MetricFilterCriteria',
    'PaginationOptions',
    'PaginatedResult',
    'IMetricRepository',
]


# Generic type variable for paginated results
T = TypeVar('T')


@dataclass
class MetricFilterCriteria:
    """Filter criteria for querying Metric entities"""
    user_id: Optional[UUID] = None
    type: Optional[MetricType] = None


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


class IMetricRepository(ABC):
    """
    Repository interface for Metric aggregate
    Implements the Repository pattern from DDD
    """

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[Metric]:
        """
        Find a Metric by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            The Metric or None if not found
        """
        pass

    @abstractmethod
    async def find_all(
        self, 
        criteria: Optional[MetricFilterCriteria] = None
    ) -> List[Metric]:
        """
        Find all Metric entities matching the given criteria
        
        Args:
            criteria: Optional filtering criteria
            
        Returns:
            List of matching Metric entities
        """
        pass

    @abstractmethod
    async def save(self, metric: Metric) -> Metric:
        """
        Save a Metric (create or update)
        
        Args:
            metric: The Metric to save
            
        Returns:
            The saved Metric
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """
        Delete a Metric by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, id: UUID) -> bool:
        """
        Check if a Metric exists by its unique identifier
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists
        """
        pass

    @abstractmethod
    async def count(
        self, 
        criteria: Optional[MetricFilterCriteria] = None
    ) -> int:
        """
        Count Metric entities matching the given criteria
        
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
        criteria: Optional[MetricFilterCriteria] = None
    ) -> PaginatedResult[Metric]:
        """
        Find Metric entities with pagination
        
        Args:
            options: Pagination options
            criteria: Optional filtering criteria
            
        Returns:
            Paginated result
        """
        pass
