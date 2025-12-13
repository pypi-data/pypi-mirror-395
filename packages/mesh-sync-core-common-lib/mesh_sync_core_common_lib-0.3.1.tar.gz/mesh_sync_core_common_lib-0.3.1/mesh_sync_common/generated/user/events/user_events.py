# AUTO-GENERATED - DO NOT EDIT
# Generated from: user/domain/user.agg.yaml
"""
Domain Events for User
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Type, Union


__all__ = [
    'UserDomainEvent',
    'UserCreatedEvent',
    'UserProfileUpdatedEvent',
    'UserSubscriptionChangedEvent',
    'UserPreferencesUpdatedEvent',
    'UserLoggedInEvent',
    'UserRoleChangedEvent',
    'OnboardingStartedEvent',
    'OnboardingStepCompletedEvent',
    'OnboardingCompletedEvent',
    'OnboardingSkippedEvent',
    'UserEvent',
    'EVENT_REGISTRY',
    'deserialize_event',
]


@dataclass(frozen=True)
class UserDomainEvent:
    """Base class for all User domain events"""
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
    def from_dict(cls, data: Dict[str, Any]) -> 'UserDomainEvent':
        """Deserialize from dictionary. Override in subclasses."""
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on']) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
        )



@dataclass(frozen=True)
class UserCreatedEvent(UserDomainEvent):
    """User account was created"""
    user_id: str
    email: str
    name: str
    role: UserRole

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserCreatedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            user_id=data['user_id'],
            email=data['email'],
            name=data['name'],
            role=data['role'],
        )


@dataclass(frozen=True)
class UserProfileUpdatedEvent(UserDomainEvent):
    """User profile was updated"""
    user_id: str
    updates: object

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'user_id': self.user_id,
            'updates': self.updates,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfileUpdatedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            user_id=data['user_id'],
            updates=data['updates'],
        )


@dataclass(frozen=True)
class UserSubscriptionChangedEvent(UserDomainEvent):
    """User subscription changed"""
    user_id: str
    subscription_id: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'user_id': self.user_id,
            'subscription_id': self.subscription_id,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserSubscriptionChangedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            user_id=data['user_id'],
            subscription_id=data['subscription_id'],
        )


@dataclass(frozen=True)
class UserPreferencesUpdatedEvent(UserDomainEvent):
    """User preferences were updated"""
    user_id: str
    preferences: object

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'user_id': self.user_id,
            'preferences': self.preferences,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserPreferencesUpdatedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            user_id=data['user_id'],
            preferences=data['preferences'],
        )


@dataclass(frozen=True)
class UserLoggedInEvent(UserDomainEvent):
    """User logged in"""
    user_id: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'user_id': self.user_id,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserLoggedInEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            user_id=data['user_id'],
        )


@dataclass(frozen=True)
class UserRoleChangedEvent(UserDomainEvent):
    """User role changed"""
    user_id: str
    old_role: UserRole
    new_role: UserRole

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'user_id': self.user_id,
            'old_role': self.old_role,
            'new_role': self.new_role,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserRoleChangedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            user_id=data['user_id'],
            old_role=data['old_role'],
            new_role=data['new_role'],
        )


@dataclass(frozen=True)
class OnboardingStartedEvent(UserDomainEvent):
    """User started onboarding"""
    user_id: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'user_id': self.user_id,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OnboardingStartedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            user_id=data['user_id'],
        )


@dataclass(frozen=True)
class OnboardingStepCompletedEvent(UserDomainEvent):
    """User completed an onboarding step"""
    user_id: str
    step_id: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'user_id': self.user_id,
            'step_id': self.step_id,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OnboardingStepCompletedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            user_id=data['user_id'],
            step_id=data['step_id'],
        )


@dataclass(frozen=True)
class OnboardingCompletedEvent(UserDomainEvent):
    """User completed all onboarding steps"""
    user_id: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'user_id': self.user_id,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OnboardingCompletedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            user_id=data['user_id'],
        )


@dataclass(frozen=True)
class OnboardingSkippedEvent(UserDomainEvent):
    """User skipped onboarding"""
    user_id: str

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            'user_id': self.user_id,
        })
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OnboardingSkippedEvent':
        """Deserialize event from dictionary.
        
        Raises:
            KeyError: If required fields are missing
            ValueError: If enum values are invalid
        """
        return cls(
            aggregate_id=data['aggregate_id'],
            occurred_on=datetime.fromisoformat(data['occurred_on'].replace('Z', '+00:00')) if isinstance(data.get('occurred_on'), str) else data.get('occurred_on', datetime.utcnow()),
            version=data.get('version', 1),
            user_id=data['user_id'],
        )



# Union type helper (for type hints)
UserEvent = Union[UserCreatedEvent, UserProfileUpdatedEvent, UserSubscriptionChangedEvent, UserPreferencesUpdatedEvent, UserLoggedInEvent, UserRoleChangedEvent, OnboardingStartedEvent, OnboardingStepCompletedEvent, OnboardingCompletedEvent, OnboardingSkippedEvent]


# Event registry for polymorphic deserialization
EVENT_REGISTRY: Dict[str, Type[UserDomainEvent]] = {
    'UserCreatedEvent': UserCreatedEvent,
    'UserProfileUpdatedEvent': UserProfileUpdatedEvent,
    'UserSubscriptionChangedEvent': UserSubscriptionChangedEvent,
    'UserPreferencesUpdatedEvent': UserPreferencesUpdatedEvent,
    'UserLoggedInEvent': UserLoggedInEvent,
    'UserRoleChangedEvent': UserRoleChangedEvent,
    'OnboardingStartedEvent': OnboardingStartedEvent,
    'OnboardingStepCompletedEvent': OnboardingStepCompletedEvent,
    'OnboardingCompletedEvent': OnboardingCompletedEvent,
    'OnboardingSkippedEvent': OnboardingSkippedEvent,
}


def deserialize_event(data: Dict[str, Any]) -> UserDomainEvent:
    """
    Deserialize any User event from dictionary using event_type discriminator.
    
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

