# AUTO-GENERATED - DO NOT EDIT
# Generated from: marketplace/domain/marketplace_item.agg.yaml
"""
Domain Events for MarketplaceItem
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Type, Union

from mesh_sync_common.generated.marketplace.marketplace_item_status_base import MarketplaceItemStatus


__all__ = [
    'MarketplaceItemDomainEvent',
    'MarketplaceItemCreatedEvent',
    'MarketplaceItemMarkedForSyncEvent',
    'MarketplaceItemStatusChangedEvent',
    'MarketplaceItemSyncSucceededEvent',
    'MarketplaceItemSyncFailedEvent',
    'MarketplaceItemEvent',
    'EVENT_REGISTRY',
    'deserialize_event',
]


@dataclass(frozen=True)
class MarketplaceItemDomainEvent:
    """Base class for all MarketplaceItem domain events"""
    aggregate_id: str
    occurred_on: datetime = field(default_factory=datetime.utcnow)
    version: int = 1  # Event schema version for evolution

    @property
    def event_type(self) -> str:
        return self.__class__.__name__

    def to_dict(self) -> Dict[str, Any]:
        return {
            'event_type': self.event_type,
            'aggregate_id': self.aggregate_id,
            'occurred_on': self.occurred_on.isoformat(),
            'version': self.version,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketplaceItemDomainEvent':
        """Deserialize from dictionary. Override in subclasses."""
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on']) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
        )



@dataclass(frozen=True)
class MarketplaceItemCreatedEvent(MarketplaceItemDomainEvent):
    """Marketplace item was created"""
    item_id: str
    model_id: str
    marketplace: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'item_id': self.item_id,
            'model_id': self.model_id,
            'marketplace': self.marketplace,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketplaceItemCreatedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            item_id=data['item_id'],
            model_id=data['model_id'],
            marketplace=data['marketplace'],
        )


@dataclass(frozen=True)
class MarketplaceItemMarkedForSyncEvent(MarketplaceItemDomainEvent):
    """Item was marked for synchronization"""
    item_id: str
    marketplace: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'item_id': self.item_id,
            'marketplace': self.marketplace,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketplaceItemMarkedForSyncEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            item_id=data['item_id'],
            marketplace=data['marketplace'],
        )


@dataclass(frozen=True)
class MarketplaceItemStatusChangedEvent(MarketplaceItemDomainEvent):
    """Item status changed"""
    item_id: str
    old_status: MarketplaceItemStatus
    new_status: MarketplaceItemStatus

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'item_id': self.item_id,
            'old_status': self.old_status.value if self.old_status else None,
            'new_status': self.new_status.value if self.new_status else None,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketplaceItemStatusChangedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            item_id=data['item_id'],
            old_status=MarketplaceItemStatus(data['old_status']) if data.get('old_status') else None,
            new_status=MarketplaceItemStatus(data['new_status']) if data.get('new_status') else None,
        )


@dataclass(frozen=True)
class MarketplaceItemSyncSucceededEvent(MarketplaceItemDomainEvent):
    """Sync with marketplace succeeded"""
    item_id: str
    marketplace: str
    marketplace_specific_id: str
    url: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'item_id': self.item_id,
            'marketplace': self.marketplace,
            'marketplace_specific_id': self.marketplace_specific_id,
            'url': self.url,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketplaceItemSyncSucceededEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            item_id=data['item_id'],
            marketplace=data['marketplace'],
            marketplace_specific_id=data['marketplace_specific_id'],
            url=data['url'],
        )


@dataclass(frozen=True)
class MarketplaceItemSyncFailedEvent(MarketplaceItemDomainEvent):
    """Sync with marketplace failed"""
    item_id: str
    marketplace: str
    error: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'item_id': self.item_id,
            'marketplace': self.marketplace,
            'error': self.error,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketplaceItemSyncFailedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            item_id=data['item_id'],
            marketplace=data['marketplace'],
            error=data['error'],
        )



# Union type helper (for type hints)
MarketplaceItemEvent = Union[MarketplaceItemCreatedEvent, MarketplaceItemMarkedForSyncEvent, MarketplaceItemStatusChangedEvent, MarketplaceItemSyncSucceededEvent, MarketplaceItemSyncFailedEvent]


# Event registry for polymorphic deserialization
EVENT_REGISTRY: Dict[str, Type[MarketplaceItemDomainEvent]] = {
    'MarketplaceItemCreatedEvent': MarketplaceItemCreatedEvent,
    'MarketplaceItemMarkedForSyncEvent': MarketplaceItemMarkedForSyncEvent,
    'MarketplaceItemStatusChangedEvent': MarketplaceItemStatusChangedEvent,
    'MarketplaceItemSyncSucceededEvent': MarketplaceItemSyncSucceededEvent,
    'MarketplaceItemSyncFailedEvent': MarketplaceItemSyncFailedEvent,
}


def deserialize_event(data: Dict[str, Any]) -> MarketplaceItemDomainEvent:
    """
    Deserialize any MarketplaceItem event from dictionary using event_type discriminator.
    
    Args:
        data: Dictionary containing event data with 'event_type' key
        
    Returns:
        The deserialized event instance
        
    Raises:
        ValueError: If event_type is unknown
    """
    event_type = data.get('event_type')
    if event_type not in EVENT_REGISTRY:
        raise ValueError(f"Unknown event type: {event_type}. Valid types: {list(EVENT_REGISTRY.keys())}")
    return EVENT_REGISTRY[event_type].from_dict(data)

