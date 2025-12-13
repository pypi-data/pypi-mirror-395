"""
Base Aggregate for Tag
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from uuid import UUID

from datetime import datetime


class TagBase:
    """
    Represents a user-defined tag for organizing models
    """
    
    def __init__(
        self,
        id: UUID,
        
        name: str,
        
        userId: UUID,
        
        createdAt: datetime = None,
        
        updatedAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            name=name,
            
            userId=userId,
            
            createdAt=createdAt,
            
            updatedAt=updatedAt,
            
        )
        
        self._id = id
        
        self._name = name
        
        self._userId = userId
        
        self._createdAt = createdAt
        
        self._updatedAt = updatedAt
        

    def _validate(self, **kwargs) -> None:
        """Validate all required fields and constraints"""
        errors = []
        
        # Identity validation
        if kwargs.get('id') is None:
            errors.append('id is required')
        
        
        
        # name: required field
        if kwargs.get('name') is None:
            errors.append('name is required')
        
        
        
        
        
        
        # userId: required field
        if kwargs.get('userId') is None:
            errors.append('userId is required')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if errors:
            raise ValueError('; '.join(errors))

    @property
    def id(self) -> UUID:
        return self._id

    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        self._name = value
    
    @property
    def userId(self) -> UUID:
        return self._userId
    
    @userId.setter
    def userId(self, value: UUID):
        self._userId = value
    
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
        if not isinstance(other, TagBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"Tag(id={self.id})"
