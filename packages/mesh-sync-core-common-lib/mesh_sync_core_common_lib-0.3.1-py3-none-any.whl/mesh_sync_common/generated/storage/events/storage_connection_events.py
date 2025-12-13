# AUTO-GENERATED - DO NOT EDIT
# Generated from: storage/domain/storage_connection.agg.yaml
"""
Domain Events for StorageConnection
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Type, Union

from mesh_sync_common.generated.storage.storage_provider_type_base import StorageProviderType

from mesh_sync_common.generated.storage.scan_status_base import ScanStatus


__all__ = [
    'StorageConnectionDomainEvent',
    'StorageConnectionCreatedEvent',
    'StorageConnectionUpdatedEvent',
    'StorageConnectionActivatedEvent',
    'StorageConnectionDeactivatedEvent',
    'StorageConnectionScanStatusUpdatedEvent',
    'StorageConnectionEvent',
    'EVENT_REGISTRY',
    'deserialize_event',
]


@dataclass(frozen=True)
class StorageConnectionDomainEvent:
    """Base class for all StorageConnection domain events"""
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
    def from_dict(cls, data: Dict[str, Any]) -> 'StorageConnectionDomainEvent':
        """Deserialize from dictionary. Override in subclasses."""
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on']) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
        )



@dataclass(frozen=True)
class StorageConnectionCreatedEvent(StorageConnectionDomainEvent):
    """Storage connection was created"""
    connection_id: str
    user_id: str
    provider_type: StorageProviderType

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'connection_id': self.connection_id,
            'user_id': self.user_id,
            'provider_type': self.provider_type.value if self.provider_type else None,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StorageConnectionCreatedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            connection_id=data['connection_id'],
            user_id=data['user_id'],
            provider_type=StorageProviderType(data['provider_type']) if data.get('provider_type') else None,
        )


@dataclass(frozen=True)
class StorageConnectionUpdatedEvent(StorageConnectionDomainEvent):
    """Storage connection was updated"""
    connection_id: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'connection_id': self.connection_id,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StorageConnectionUpdatedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            connection_id=data['connection_id'],
        )


@dataclass(frozen=True)
class StorageConnectionActivatedEvent(StorageConnectionDomainEvent):
    """Storage connection was activated"""
    connection_id: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'connection_id': self.connection_id,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StorageConnectionActivatedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            connection_id=data['connection_id'],
        )


@dataclass(frozen=True)
class StorageConnectionDeactivatedEvent(StorageConnectionDomainEvent):
    """Storage connection was deactivated"""
    connection_id: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'connection_id': self.connection_id,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StorageConnectionDeactivatedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            connection_id=data['connection_id'],
        )


@dataclass(frozen=True)
class StorageConnectionScanStatusUpdatedEvent(StorageConnectionDomainEvent):
    """Scan status was updated"""
    connection_id: str
    status: ScanStatus
    error: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'connection_id': self.connection_id,
            'status': self.status.value if self.status else None,
            'error': self.error,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StorageConnectionScanStatusUpdatedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            connection_id=data['connection_id'],
            status=ScanStatus(data['status']) if data.get('status') else None,
            error=data['error'],
        )



# Union type helper (for type hints)
StorageConnectionEvent = Union[StorageConnectionCreatedEvent, StorageConnectionUpdatedEvent, StorageConnectionActivatedEvent, StorageConnectionDeactivatedEvent, StorageConnectionScanStatusUpdatedEvent]


# Event registry for polymorphic deserialization
EVENT_REGISTRY: Dict[str, Type[StorageConnectionDomainEvent]] = {
    'StorageConnectionCreatedEvent': StorageConnectionCreatedEvent,
    'StorageConnectionUpdatedEvent': StorageConnectionUpdatedEvent,
    'StorageConnectionActivatedEvent': StorageConnectionActivatedEvent,
    'StorageConnectionDeactivatedEvent': StorageConnectionDeactivatedEvent,
    'StorageConnectionScanStatusUpdatedEvent': StorageConnectionScanStatusUpdatedEvent,
}


def deserialize_event(data: Dict[str, Any]) -> StorageConnectionDomainEvent:
    """
    Deserialize any StorageConnection event from dictionary using event_type discriminator.
    
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

