"""
Base Aggregate for Texture
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from uuid import UUID

from mesh_sync_common.generated.texture.texture_type_base import TextureType

from datetime import datetime


class TextureBase:
    """
    Represents a texture or environment image
    """
    
    def __init__(
        self,
        id: UUID,
        
        userId: UUID,
        
        name: str,
        
        type: TextureType,
        
        colorValue: Optional[str] = None,
        
        storageItemId: Optional[UUID] = None,
        
        description: Optional[str] = None,
        
        isPublic: bool = None,
        
        createdAt: datetime = None,
        
        updatedAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            userId=userId,
            
            name=name,
            
            type=type,
            
            colorValue=colorValue,
            
            storageItemId=storageItemId,
            
            description=description,
            
            isPublic=isPublic,
            
            createdAt=createdAt,
            
            updatedAt=updatedAt,
            
        )
        
        self._id = id
        
        self._userId = userId
        
        self._name = name
        
        self._type = type
        
        self._colorValue = colorValue
        
        self._storageItemId = storageItemId
        
        self._description = description
        
        self._isPublic = isPublic
        
        self._createdAt = createdAt
        
        self._updatedAt = updatedAt
        

    def _validate(self, **kwargs) -> None:
        """Validate all required fields and constraints"""
        errors = []
        
        # Identity validation
        if kwargs.get('id') is None:
            errors.append('id is required')
        
        
        
        # userId: required field
        if kwargs.get('userId') is None:
            errors.append('userId is required')
        
        
        
        
        
        
        # name: required field
        if kwargs.get('name') is None:
            errors.append('name is required')
        
        
        
        
        
        
        # type: required field
        if kwargs.get('type') is None:
            errors.append('type is required')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if errors:
            raise ValueError('; '.join(errors))

    @property
    def id(self) -> UUID:
        return self._id

    
    @property
    def userId(self) -> UUID:
        return self._userId
    
    @userId.setter
    def userId(self, value: UUID):
        self._userId = value
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        self._name = value
    
    @property
    def type(self) -> TextureType:
        return self._type
    
    @type.setter
    def type(self, value: TextureType):
        self._type = value
    
    @property
    def colorValue(self) -> Optional[str]:
        return self._colorValue
    
    @colorValue.setter
    def colorValue(self, value: Optional[str]):
        self._colorValue = value
    
    @property
    def storageItemId(self) -> Optional[UUID]:
        return self._storageItemId
    
    @storageItemId.setter
    def storageItemId(self, value: Optional[UUID]):
        self._storageItemId = value
    
    @property
    def description(self) -> Optional[str]:
        return self._description
    
    @description.setter
    def description(self, value: Optional[str]):
        self._description = value
    
    @property
    def isPublic(self) -> bool:
        return self._isPublic
    
    @isPublic.setter
    def isPublic(self, value: bool):
        self._isPublic = value
    
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
        if not isinstance(other, TextureBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"Texture(id={self.id})"
