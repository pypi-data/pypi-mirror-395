"""
Base Aggregate for MarketplaceItem
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from typing import List

from uuid import UUID

from mesh_sync_common.generated.marketplace.marketplace_item_status_base import MarketplaceItemStatus

from mesh_sync_common.generated.marketplace.marketplace_item_stats_base import MarketplaceItemStatsBase

from datetime import datetime


class MarketplaceItemBase:
    """
    Represents an item listed on a specific marketplace, linked to an internal Model
    """
    
    def __init__(
        self,
        id: UUID,
        
        modelId: UUID,
        
        userId: UUID,
        
        marketplace: str,
        
        title: str,
        
        description: str,
        
        price: float,
        
        currency: str,
        
        marketplaceSpecificId: str = None,
        
        externalCategoryId: str = None,
        
        status: MarketplaceItemStatus = None,
        
        url: str = None,
        
        tags: List[str] = None,
        
        stats: MarketplaceItemStatsBase = None,
        
        lastSyncTime: datetime = None,
        
        syncError: str = None,
        
        createdAt: datetime = None,
        
        updatedAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            modelId=modelId,
            
            userId=userId,
            
            marketplace=marketplace,
            
            title=title,
            
            description=description,
            
            price=price,
            
            currency=currency,
            
            marketplaceSpecificId=marketplaceSpecificId,
            
            externalCategoryId=externalCategoryId,
            
            status=status,
            
            url=url,
            
            tags=tags,
            
            stats=stats,
            
            lastSyncTime=lastSyncTime,
            
            syncError=syncError,
            
            createdAt=createdAt,
            
            updatedAt=updatedAt,
            
        )
        
        self._id = id
        
        self._modelId = modelId
        
        self._userId = userId
        
        self._marketplace = marketplace
        
        self._title = title
        
        self._description = description
        
        self._price = price
        
        self._currency = currency
        
        self._marketplaceSpecificId = marketplaceSpecificId
        
        self._externalCategoryId = externalCategoryId
        
        self._status = status
        
        self._url = url
        
        self._tags = tags
        
        self._stats = stats
        
        self._lastSyncTime = lastSyncTime
        
        self._syncError = syncError
        
        self._createdAt = createdAt
        
        self._updatedAt = updatedAt
        

    def _validate(self, **kwargs) -> None:
        """Validate all required fields and constraints"""
        errors = []
        
        # Identity validation
        if kwargs.get('id') is None:
            errors.append('id is required')
        
        
        
        # modelId: required field
        if kwargs.get('modelId') is None:
            errors.append('modelId is required')
        
        
        
        
        
        
        # userId: required field
        if kwargs.get('userId') is None:
            errors.append('userId is required')
        
        
        
        
        
        
        # marketplace: required field
        if kwargs.get('marketplace') is None:
            errors.append('marketplace is required')
        
        
        
        
        
        
        # title: required field
        if kwargs.get('title') is None:
            errors.append('title is required')
        
        
        
        
        
        
        # description: required field
        if kwargs.get('description') is None:
            errors.append('description is required')
        
        
        
        
        
        
        # price: required field
        if kwargs.get('price') is None:
            errors.append('price is required')
        
        
        # price: min constraint
        if kwargs.get('price') is not None and kwargs.get('price') < 0:
            errors.append('price must be >= 0')
        
        
        
        
        
        # currency: required field
        if kwargs.get('currency') is None:
            errors.append('currency is required')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if errors:
            raise ValueError('; '.join(errors))

    @property
    def id(self) -> UUID:
        return self._id

    
    @property
    def modelId(self) -> UUID:
        return self._modelId
    
    @modelId.setter
    def modelId(self, value: UUID):
        self._modelId = value
    
    @property
    def userId(self) -> UUID:
        return self._userId
    
    @userId.setter
    def userId(self, value: UUID):
        self._userId = value
    
    @property
    def marketplace(self) -> str:
        return self._marketplace
    
    @marketplace.setter
    def marketplace(self, value: str):
        self._marketplace = value
    
    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, value: str):
        self._title = value
    
    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str):
        self._description = value
    
    @property
    def price(self) -> float:
        return self._price
    
    @price.setter
    def price(self, value: float):
        self._price = value
    
    @property
    def currency(self) -> str:
        return self._currency
    
    @currency.setter
    def currency(self, value: str):
        self._currency = value
    
    @property
    def marketplaceSpecificId(self) -> str:
        return self._marketplaceSpecificId
    
    @marketplaceSpecificId.setter
    def marketplaceSpecificId(self, value: str):
        self._marketplaceSpecificId = value
    
    @property
    def externalCategoryId(self) -> str:
        return self._externalCategoryId
    
    @externalCategoryId.setter
    def externalCategoryId(self, value: str):
        self._externalCategoryId = value
    
    @property
    def status(self) -> MarketplaceItemStatus:
        return self._status
    
    @status.setter
    def status(self, value: MarketplaceItemStatus):
        self._status = value
    
    @property
    def url(self) -> str:
        return self._url
    
    @url.setter
    def url(self, value: str):
        self._url = value
    
    @property
    def tags(self) -> List[str]:
        return self._tags
    
    @tags.setter
    def tags(self, value: List[str]):
        self._tags = value
    
    @property
    def stats(self) -> MarketplaceItemStatsBase:
        return self._stats
    
    @stats.setter
    def stats(self, value: MarketplaceItemStatsBase):
        self._stats = value
    
    @property
    def lastSyncTime(self) -> datetime:
        return self._lastSyncTime
    
    @lastSyncTime.setter
    def lastSyncTime(self, value: datetime):
        self._lastSyncTime = value
    
    @property
    def syncError(self) -> str:
        return self._syncError
    
    @syncError.setter
    def syncError(self, value: str):
        self._syncError = value
    
    @property
    def createdAt(self) -> datetime:
        return self._createdAt
    
    @createdAt.setter
    def createdAt(self, value: datetime):
        self._createdAt = value
    
    @property
    def updatedAt(self) -> datetime:
        return self._updatedAt
    
    @updatedAt.setter
    def updatedAt(self, value: datetime):
        self._updatedAt = value
    

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MarketplaceItemBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"MarketplaceItem(id={self.id})"
