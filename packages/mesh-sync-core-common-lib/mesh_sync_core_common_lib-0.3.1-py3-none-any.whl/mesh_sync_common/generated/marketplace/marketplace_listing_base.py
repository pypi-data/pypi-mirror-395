"""
Base Aggregate for MarketplaceListing
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from typing import List

from uuid import UUID

from mesh_sync_common.generated.marketplace.marketplace_item_stats_base import MarketplaceItemStatsBase

from mesh_sync_common.generated.marketplace.marketplace_listing_status_base import MarketplaceListingStatus

from mesh_sync_common.generated.marketplace.etsy_listing_metadata_base import EtsyListingMetadataBase

from datetime import datetime


class MarketplaceListingBase:
    """
    Represents a listing on an external marketplace
    """
    
    def __init__(
        self,
        id: UUID,
        
        modelId: UUID,
        
        marketplaceId: str,
        
        marketplaceSpecificId: str,
        
        title: str,
        
        description: str,
        
        price: float,
        
        currency: str,
        
        quantity: int,
        
        stats: MarketplaceItemStatsBase,
        
        url: Optional[str] = None,
        
        tags: List[str] = None,
        
        taxonomyId: Optional[str] = None,
        
        isDigital: bool = None,
        
        status: MarketplaceListingStatus = None,
        
        etsyMetadata: Optional[EtsyListingMetadataBase] = None,
        
        lastSyncAt: Optional[datetime] = None,
        
        createdAt: datetime = None,
        
        updatedAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            modelId=modelId,
            
            marketplaceId=marketplaceId,
            
            marketplaceSpecificId=marketplaceSpecificId,
            
            title=title,
            
            description=description,
            
            price=price,
            
            currency=currency,
            
            quantity=quantity,
            
            stats=stats,
            
            url=url,
            
            tags=tags,
            
            taxonomyId=taxonomyId,
            
            isDigital=isDigital,
            
            status=status,
            
            etsyMetadata=etsyMetadata,
            
            lastSyncAt=lastSyncAt,
            
            createdAt=createdAt,
            
            updatedAt=updatedAt,
            
        )
        
        self._id = id
        
        self._modelId = modelId
        
        self._marketplaceId = marketplaceId
        
        self._marketplaceSpecificId = marketplaceSpecificId
        
        self._title = title
        
        self._description = description
        
        self._price = price
        
        self._currency = currency
        
        self._quantity = quantity
        
        self._stats = stats
        
        self._url = url
        
        self._tags = tags
        
        self._taxonomyId = taxonomyId
        
        self._isDigital = isDigital
        
        self._status = status
        
        self._etsyMetadata = etsyMetadata
        
        self._lastSyncAt = lastSyncAt
        
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
        
        
        
        
        
        
        # marketplaceId: required field
        if kwargs.get('marketplaceId') is None:
            errors.append('marketplaceId is required')
        
        
        
        
        
        
        # marketplaceSpecificId: required field
        if kwargs.get('marketplaceSpecificId') is None:
            errors.append('marketplaceSpecificId is required')
        
        
        
        
        
        
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
        
        
        
        
        
        
        # quantity: required field
        if kwargs.get('quantity') is None:
            errors.append('quantity is required')
        
        
        # quantity: min constraint
        if kwargs.get('quantity') is not None and kwargs.get('quantity') < 0:
            errors.append('quantity must be >= 0')
        
        
        
        
        
        # stats: required field
        if kwargs.get('stats') is None:
            errors.append('stats is required')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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
    def marketplaceId(self) -> str:
        return self._marketplaceId
    
    @marketplaceId.setter
    def marketplaceId(self, value: str):
        self._marketplaceId = value
    
    @property
    def marketplaceSpecificId(self) -> str:
        return self._marketplaceSpecificId
    
    @marketplaceSpecificId.setter
    def marketplaceSpecificId(self, value: str):
        self._marketplaceSpecificId = value
    
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
    def quantity(self) -> int:
        return self._quantity
    
    @quantity.setter
    def quantity(self, value: int):
        self._quantity = value
    
    @property
    def stats(self) -> MarketplaceItemStatsBase:
        return self._stats
    
    @stats.setter
    def stats(self, value: MarketplaceItemStatsBase):
        self._stats = value
    
    @property
    def url(self) -> Optional[str]:
        return self._url
    
    @url.setter
    def url(self, value: Optional[str]):
        self._url = value
    
    @property
    def tags(self) -> List[str]:
        return self._tags
    
    @tags.setter
    def tags(self, value: List[str]):
        self._tags = value
    
    @property
    def taxonomyId(self) -> Optional[str]:
        return self._taxonomyId
    
    @taxonomyId.setter
    def taxonomyId(self, value: Optional[str]):
        self._taxonomyId = value
    
    @property
    def isDigital(self) -> bool:
        return self._isDigital
    
    @isDigital.setter
    def isDigital(self, value: bool):
        self._isDigital = value
    
    @property
    def status(self) -> MarketplaceListingStatus:
        return self._status
    
    @status.setter
    def status(self, value: MarketplaceListingStatus):
        self._status = value
    
    @property
    def etsyMetadata(self) -> Optional[EtsyListingMetadataBase]:
        return self._etsyMetadata
    
    @etsyMetadata.setter
    def etsyMetadata(self, value: Optional[EtsyListingMetadataBase]):
        self._etsyMetadata = value
    
    @property
    def lastSyncAt(self) -> Optional[datetime]:
        return self._lastSyncAt
    
    @lastSyncAt.setter
    def lastSyncAt(self, value: Optional[datetime]):
        self._lastSyncAt = value
    
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
        if not isinstance(other, MarketplaceListingBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"MarketplaceListing(id={self.id})"
