# AUTO-GENERATED - DO NOT EDIT
# Generated from: storage/domain/storage_provider_config.agg.yaml
"""
Domain Events for StorageProviderConfig
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Type, Union

from mesh_sync_common.generated.storage.storage_provider_type_base import StorageProviderType


__all__ = [
    'StorageProviderConfigDomainEvent',
    'StorageProviderConfigCreatedEvent',
    'StorageProviderConfigUpdatedEvent',
    'StorageProviderCredentialsUpdatedEvent',
    'StorageProviderModelIdentificationRulesUpdatedEvent',
    'StorageProviderConnectionStatusChangedEvent',
    'StorageProviderConfigEvent',
    'EVENT_REGISTRY',
    'deserialize_event',
]


@dataclass(frozen=True)
class StorageProviderConfigDomainEvent:
    """Base class for all StorageProviderConfig domain events"""
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
    def from_dict(cls, data: Dict[str, Any]) -> 'StorageProviderConfigDomainEvent':
        """Deserialize from dictionary. Override in subclasses."""
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on']) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
        )



@dataclass(frozen=True)
class StorageProviderConfigCreatedEvent(StorageProviderConfigDomainEvent):
    """Storage provider config was created"""
    config_id: str
    user_id: str
    type: StorageProviderType

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'config_id': self.config_id,
            'user_id': self.user_id,
            'type': self.type.value if self.type else None,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StorageProviderConfigCreatedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            config_id=data['config_id'],
            user_id=data['user_id'],
            type=StorageProviderType(data['type']) if data.get('type') else None,
        )


@dataclass(frozen=True)
class StorageProviderConfigUpdatedEvent(StorageProviderConfigDomainEvent):
    """Storage provider config was updated"""
    config_id: str
    name: str
    scan_root_path: str
    max_scan_depth: int
    configuration: object

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'config_id': self.config_id,
            'name': self.name,
            'scan_root_path': self.scan_root_path,
            'max_scan_depth': self.max_scan_depth,
            'configuration': self.configuration,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StorageProviderConfigUpdatedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            config_id=data['config_id'],
            name=data['name'],
            scan_root_path=data['scan_root_path'],
            max_scan_depth=data['max_scan_depth'],
            configuration=data['configuration'],
        )


@dataclass(frozen=True)
class StorageProviderCredentialsUpdatedEvent(StorageProviderConfigDomainEvent):
    """Provider credentials were updated"""
    config_id: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'config_id': self.config_id,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StorageProviderCredentialsUpdatedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            config_id=data['config_id'],
        )


@dataclass(frozen=True)
class StorageProviderModelIdentificationRulesUpdatedEvent(StorageProviderConfigDomainEvent):
    """Model identification rules were updated"""
    config_id: str
    rules: object

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'config_id': self.config_id,
            'rules': self.rules,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StorageProviderModelIdentificationRulesUpdatedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            config_id=data['config_id'],
            rules=data['rules'],
        )


@dataclass(frozen=True)
class StorageProviderConnectionStatusChangedEvent(StorageProviderConfigDomainEvent):
    """Connection status changed"""
    config_id: str
    is_connected: bool
    error: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'config_id': self.config_id,
            'is_connected': self.is_connected,
            'error': self.error,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StorageProviderConnectionStatusChangedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            config_id=data['config_id'],
            is_connected=data['is_connected'],
            error=data['error'],
        )



# Union type helper (for type hints)
StorageProviderConfigEvent = Union[StorageProviderConfigCreatedEvent, StorageProviderConfigUpdatedEvent, StorageProviderCredentialsUpdatedEvent, StorageProviderModelIdentificationRulesUpdatedEvent, StorageProviderConnectionStatusChangedEvent]


# Event registry for polymorphic deserialization
EVENT_REGISTRY: Dict[str, Type[StorageProviderConfigDomainEvent]] = {
    'StorageProviderConfigCreatedEvent': StorageProviderConfigCreatedEvent,
    'StorageProviderConfigUpdatedEvent': StorageProviderConfigUpdatedEvent,
    'StorageProviderCredentialsUpdatedEvent': StorageProviderCredentialsUpdatedEvent,
    'StorageProviderModelIdentificationRulesUpdatedEvent': StorageProviderModelIdentificationRulesUpdatedEvent,
    'StorageProviderConnectionStatusChangedEvent': StorageProviderConnectionStatusChangedEvent,
}


def deserialize_event(data: Dict[str, Any]) -> StorageProviderConfigDomainEvent:
    """
    Deserialize any StorageProviderConfig event from dictionary using event_type discriminator.
    
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

