"""
Base Aggregate for AssociatedMedia
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from typing import List

from uuid import UUID

from datetime import datetime


class AssociatedMediaBase:
    """
    Collection of media associated with a Model or Metamodel
    """
    
    def __init__(
        self,
        id: UUID,
        
        modelId: Optional[UUID] = None,
        
        metamodelId: Optional[UUID] = None,
        
        orderedThumbnailIds: List[UUID] = None,
        
        createdAt: datetime = None,
        
        updatedAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            modelId=modelId,
            
            metamodelId=metamodelId,
            
            orderedThumbnailIds=orderedThumbnailIds,
            
            createdAt=createdAt,
            
            updatedAt=updatedAt,
            
        )
        
        self._id = id
        
        self._modelId = modelId
        
        self._metamodelId = metamodelId
        
        self._orderedThumbnailIds = orderedThumbnailIds
        
        self._createdAt = createdAt
        
        self._updatedAt = updatedAt
        

    def _validate(self, **kwargs) -> None:
        """Validate all required fields and constraints"""
        errors = []
        
        # Identity validation
        if kwargs.get('id') is None:
            errors.append('id is required')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if errors:
            raise ValueError('; '.join(errors))

    @property
    def id(self) -> UUID:
        return self._id

    
    @property
    def modelId(self) -> Optional[UUID]:
        return self._modelId
    
    @modelId.setter
    def modelId(self, value: Optional[UUID]):
        self._modelId = value
    
    @property
    def metamodelId(self) -> Optional[UUID]:
        return self._metamodelId
    
    @metamodelId.setter
    def metamodelId(self, value: Optional[UUID]):
        self._metamodelId = value
    
    @property
    def orderedThumbnailIds(self) -> List[UUID]:
        return self._orderedThumbnailIds
    
    @orderedThumbnailIds.setter
    def orderedThumbnailIds(self, value: List[UUID]):
        self._orderedThumbnailIds = value
    
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
        if not isinstance(other, AssociatedMediaBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"AssociatedMedia(id={self.id})"
