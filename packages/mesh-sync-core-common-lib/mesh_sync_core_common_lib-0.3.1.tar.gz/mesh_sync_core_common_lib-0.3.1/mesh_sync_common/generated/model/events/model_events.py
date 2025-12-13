# AUTO-GENERATED - DO NOT EDIT
# Generated from: model/domain/model.agg.yaml
"""
Domain Events for Model
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Type, Union

from mesh_sync_common.generated.catalog.model_status_base import ModelStatus

from mesh_sync_common.generated.model.error_code_base import ErrorCode


__all__ = [
    'ModelDomainEvent',
    'ModelDiscovered',
    'ModelProcessed',
    'ModelErrorOccurred',
    'ModelStatusChanged',
    'ModelEvent',
    'EVENT_REGISTRY',
    'deserialize_event',
]


@dataclass(frozen=True)
class ModelDomainEvent:
    """Base class for all Model domain events"""
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
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelDomainEvent':
        """Deserialize from dictionary. Override in subclasses."""
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on']) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
        )



@dataclass(frozen=True)
class ModelDiscovered(ModelDomainEvent):
    """Model has been discovered in storage"""
    model_id: str
    owner_id: str
    library_id: str
    file_name: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'model_id': self.model_id,
            'owner_id': self.owner_id,
            'library_id': self.library_id,
            'file_name': self.file_name,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelDiscovered':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            model_id=data['model_id'],
            owner_id=data['owner_id'],
            library_id=data['library_id'],
            file_name=data['file_name'],
        )


@dataclass(frozen=True)
class ModelProcessed(ModelDomainEvent):
    """Model has been successfully processed"""
    model_id: str
    status: ModelStatus

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'model_id': self.model_id,
            'status': self.status.value if self.status else None,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelProcessed':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            model_id=data['model_id'],
            status=ModelStatus(data['status']) if data.get('status') else None,
        )


@dataclass(frozen=True)
class ModelErrorOccurred(ModelDomainEvent):
    """An error occurred during model processing"""
    model_id: str
    error_code: ErrorCode
    error_message: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'model_id': self.model_id,
            'error_code': self.error_code.value if self.error_code else None,
            'error_message': self.error_message,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelErrorOccurred':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            model_id=data['model_id'],
            error_code=ErrorCode(data['error_code']) if data.get('error_code') else None,
            error_message=data['error_message'],
        )


@dataclass(frozen=True)
class ModelStatusChanged(ModelDomainEvent):
    """Model status has changed"""
    model_id: str
    old_status: ModelStatus
    new_status: ModelStatus

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'model_id': self.model_id,
            'old_status': self.old_status.value if self.old_status else None,
            'new_status': self.new_status.value if self.new_status else None,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelStatusChanged':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            model_id=data['model_id'],
            old_status=ModelStatus(data['old_status']) if data.get('old_status') else None,
            new_status=ModelStatus(data['new_status']) if data.get('new_status') else None,
        )



# Union type helper (for type hints)
ModelEvent = Union[ModelDiscovered, ModelProcessed, ModelErrorOccurred, ModelStatusChanged]


# Event registry for polymorphic deserialization
EVENT_REGISTRY: Dict[str, Type[ModelDomainEvent]] = {
    'ModelDiscovered': ModelDiscovered,
    'ModelProcessed': ModelProcessed,
    'ModelErrorOccurred': ModelErrorOccurred,
    'ModelStatusChanged': ModelStatusChanged,
}


def deserialize_event(data: Dict[str, Any]) -> ModelDomainEvent:
    """
    Deserialize any Model event from dictionary using event_type discriminator.
    
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

