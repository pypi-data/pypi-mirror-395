"""
Base Aggregate for User
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from mesh_sync_common.generated.user.user_preferences_base import UserPreferencesBase

from mesh_sync_common.generated.user.user_role_base import UserRole

from datetime import datetime


class UserBase:
    """
    Represents a user account in the system
    """
    
    def __init__(
        self,
        id: UUID,
        
        email: str,
        
        name: str,
        
        preferences: UserPreferencesBase,
        
        role: UserRole = None,
        
        subscriptionId: str = None,
        
        lastLogin: datetime = None,
        
        createdAt: datetime = None,
        
        updatedAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            email=email,
            
            name=name,
            
            preferences=preferences,
            
            role=role,
            
            subscriptionId=subscriptionId,
            
            lastLogin=lastLogin,
            
            createdAt=createdAt,
            
            updatedAt=updatedAt,
            
        )
        
        self._id = id
        
        self._email = email
        
        self._name = name
        
        self._preferences = preferences
        
        self._role = role
        
        self._subscriptionId = subscriptionId
        
        self._lastLogin = lastLogin
        
        self._createdAt = createdAt
        
        self._updatedAt = updatedAt
        

    def _validate(self, **kwargs) -> None:
        """Validate all required fields and constraints"""
        errors = []
        
        # Identity validation
        if kwargs.get('id') is None:
            errors.append('id is required')
        
        
        
        # email: required field
        if kwargs.get('email') is None:
            errors.append('email is required')
        
        
        
        
        
        
        # name: required field
        if kwargs.get('name') is None:
            errors.append('name is required')
        
        
        
        
        
        
        # preferences: required field
        if kwargs.get('preferences') is None:
            errors.append('preferences is required')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if errors:
            raise ValueError('; '.join(errors))

    @property
    def id(self) -> UUID:
        return self._id

    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        self._email = value
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        self._name = value
    
    @property
    def preferences(self) -> UserPreferencesBase:
        return self._preferences
    
    @preferences.setter
    def preferences(self, value: UserPreferencesBase):
        self._preferences = value
    
    @property
    def role(self) -> UserRole:
        return self._role
    
    @role.setter
    def role(self, value: UserRole):
        self._role = value
    
    @property
    def subscriptionId(self) -> str:
        return self._subscriptionId
    
    @subscriptionId.setter
    def subscriptionId(self, value: str):
        self._subscriptionId = value
    
    @property
    def lastLogin(self) -> datetime:
        return self._lastLogin
    
    @lastLogin.setter
    def lastLogin(self, value: datetime):
        self._lastLogin = value
    
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
        if not isinstance(other, UserBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"User(id={self.id})"
