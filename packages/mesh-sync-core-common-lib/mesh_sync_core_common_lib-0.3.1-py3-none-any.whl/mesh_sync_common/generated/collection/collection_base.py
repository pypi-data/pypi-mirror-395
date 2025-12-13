"""
Base Aggregate for Collection
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from typing import List

from uuid import UUID

from mesh_sync_common.generated.collection.thumbnail_type_base import ThumbnailType

from mesh_sync_common.generated.collection.thumbnail_status_base import ThumbnailStatus

from datetime import datetime


class CollectionBase:
    """
    Represents a user-defined collection of models
    """
    
    def __init__(
        self,
        id: UUID,
        
        userId: UUID,
        
        name: str,
        
        description: Optional[str] = None,
        
        isPublic: bool = None,
        
        thumbnailType: ThumbnailType = None,
        
        thumbnailProcessedPath: Optional[str] = None,
        
        thumbnailStatus: ThumbnailStatus = None,
        
        thumbnailSourcePath: Optional[str] = None,
        
        thumbnailSourceConnectionId: Optional[UUID] = None,
        
        modelIds: List[UUID] = None,
        
        createdAt: datetime = None,
        
        updatedAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            userId=userId,
            
            name=name,
            
            description=description,
            
            isPublic=isPublic,
            
            thumbnailType=thumbnailType,
            
            thumbnailProcessedPath=thumbnailProcessedPath,
            
            thumbnailStatus=thumbnailStatus,
            
            thumbnailSourcePath=thumbnailSourcePath,
            
            thumbnailSourceConnectionId=thumbnailSourceConnectionId,
            
            modelIds=modelIds,
            
            createdAt=createdAt,
            
            updatedAt=updatedAt,
            
        )
        
        self._id = id
        
        self._userId = userId
        
        self._name = name
        
        self._description = description
        
        self._isPublic = isPublic
        
        self._thumbnailType = thumbnailType
        
        self._thumbnailProcessedPath = thumbnailProcessedPath
        
        self._thumbnailStatus = thumbnailStatus
        
        self._thumbnailSourcePath = thumbnailSourcePath
        
        self._thumbnailSourceConnectionId = thumbnailSourceConnectionId
        
        self._modelIds = modelIds
        
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
    def thumbnailType(self) -> ThumbnailType:
        return self._thumbnailType
    
    @thumbnailType.setter
    def thumbnailType(self, value: ThumbnailType):
        self._thumbnailType = value
    
    @property
    def thumbnailProcessedPath(self) -> Optional[str]:
        return self._thumbnailProcessedPath
    
    @thumbnailProcessedPath.setter
    def thumbnailProcessedPath(self, value: Optional[str]):
        self._thumbnailProcessedPath = value
    
    @property
    def thumbnailStatus(self) -> ThumbnailStatus:
        return self._thumbnailStatus
    
    @thumbnailStatus.setter
    def thumbnailStatus(self, value: ThumbnailStatus):
        self._thumbnailStatus = value
    
    @property
    def thumbnailSourcePath(self) -> Optional[str]:
        return self._thumbnailSourcePath
    
    @thumbnailSourcePath.setter
    def thumbnailSourcePath(self, value: Optional[str]):
        self._thumbnailSourcePath = value
    
    @property
    def thumbnailSourceConnectionId(self) -> Optional[UUID]:
        return self._thumbnailSourceConnectionId
    
    @thumbnailSourceConnectionId.setter
    def thumbnailSourceConnectionId(self, value: Optional[UUID]):
        self._thumbnailSourceConnectionId = value
    
    @property
    def modelIds(self) -> List[UUID]:
        return self._modelIds
    
    @modelIds.setter
    def modelIds(self, value: List[UUID]):
        self._modelIds = value
    
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
        if not isinstance(other, CollectionBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"Collection(id={self.id})"
