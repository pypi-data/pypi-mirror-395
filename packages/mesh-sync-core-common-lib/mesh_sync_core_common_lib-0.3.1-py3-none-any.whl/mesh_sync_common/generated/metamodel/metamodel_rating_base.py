"""
Base Aggregate for MetamodelRating
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from uuid import UUID

from mesh_sync_common.generated.metamodel.metamodel_rating_vo_base import MetamodelRatingVOBase

from datetime import datetime


class MetamodelRatingBase:
    """
    Represents a user's rating of a metamodel
    """
    
    def __init__(
        self,
        id: UUID,
        
        userId: UUID,
        
        metamodelId: UUID,
        
        rating: MetamodelRatingVOBase,
        
        createdAt: datetime = None,
        
        updatedAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            userId=userId,
            
            metamodelId=metamodelId,
            
            rating=rating,
            
            createdAt=createdAt,
            
            updatedAt=updatedAt,
            
        )
        
        self._id = id
        
        self._userId = userId
        
        self._metamodelId = metamodelId
        
        self._rating = rating
        
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
        
        
        
        
        
        
        # metamodelId: required field
        if kwargs.get('metamodelId') is None:
            errors.append('metamodelId is required')
        
        
        
        
        
        
        # rating: required field
        if kwargs.get('rating') is None:
            errors.append('rating is required')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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
    def metamodelId(self) -> UUID:
        return self._metamodelId
    
    @metamodelId.setter
    def metamodelId(self, value: UUID):
        self._metamodelId = value
    
    @property
    def rating(self) -> MetamodelRatingVOBase:
        return self._rating
    
    @rating.setter
    def rating(self, value: MetamodelRatingVOBase):
        self._rating = value
    
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
        if not isinstance(other, MetamodelRatingBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"MetamodelRating(id={self.id})"
