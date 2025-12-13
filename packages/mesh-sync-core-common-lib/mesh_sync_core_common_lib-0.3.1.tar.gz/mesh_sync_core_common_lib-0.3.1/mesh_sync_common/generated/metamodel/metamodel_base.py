"""
Base Aggregate for Metamodel
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from typing import List

from uuid import UUID

from mesh_sync_common.generated.metamodel.metamodel_status_base import MetamodelStatus

from datetime import datetime


class MetamodelBase:
    """
    Represents a group of related storage items that form a metamodel
    """
    
    def __init__(
        self,
        id: UUID,
        
        name: str,
        
        ownerId: UUID,
        
        libraryId: UUID,
        
        status: MetamodelStatus = None,
        
        storageItemIds: List[UUID] = None,
        
        confidenceScore: Optional[float] = None,
        
        sellabilityScore: Optional[float] = None,
        
        associatedMediaId: Optional[UUID] = None,
        
        internalId: Optional[str] = None,
        
        parentMetamodelId: Optional[UUID] = None,
        
        childMetamodelIds: List[UUID] = None,
        
        createdAt: datetime = None,
        
        updatedAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            name=name,
            
            ownerId=ownerId,
            
            libraryId=libraryId,
            
            status=status,
            
            storageItemIds=storageItemIds,
            
            confidenceScore=confidenceScore,
            
            sellabilityScore=sellabilityScore,
            
            associatedMediaId=associatedMediaId,
            
            internalId=internalId,
            
            parentMetamodelId=parentMetamodelId,
            
            childMetamodelIds=childMetamodelIds,
            
            createdAt=createdAt,
            
            updatedAt=updatedAt,
            
        )
        
        self._id = id
        
        self._name = name
        
        self._ownerId = ownerId
        
        self._libraryId = libraryId
        
        self._status = status
        
        self._storageItemIds = storageItemIds
        
        self._confidenceScore = confidenceScore
        
        self._sellabilityScore = sellabilityScore
        
        self._associatedMediaId = associatedMediaId
        
        self._internalId = internalId
        
        self._parentMetamodelId = parentMetamodelId
        
        self._childMetamodelIds = childMetamodelIds
        
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
        
        
        
        
        
        
        # ownerId: required field
        if kwargs.get('ownerId') is None:
            errors.append('ownerId is required')
        
        
        
        
        
        
        # libraryId: required field
        if kwargs.get('libraryId') is None:
            errors.append('libraryId is required')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # confidenceScore: min constraint
        if kwargs.get('confidenceScore') is not None and kwargs.get('confidenceScore') < 0:
            errors.append('confidenceScore must be >= 0')
        
        
        # confidenceScore: max constraint
        if kwargs.get('confidenceScore') is not None and kwargs.get('confidenceScore') > 1:
            errors.append('confidenceScore must be <= 1')
        
        
        
        
        
        # sellabilityScore: min constraint
        if kwargs.get('sellabilityScore') is not None and kwargs.get('sellabilityScore') < 0:
            errors.append('sellabilityScore must be >= 0')
        
        
        # sellabilityScore: max constraint
        if kwargs.get('sellabilityScore') is not None and kwargs.get('sellabilityScore') > 1:
            errors.append('sellabilityScore must be <= 1')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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
    def ownerId(self) -> UUID:
        return self._ownerId
    
    @ownerId.setter
    def ownerId(self, value: UUID):
        self._ownerId = value
    
    @property
    def libraryId(self) -> UUID:
        return self._libraryId
    
    @libraryId.setter
    def libraryId(self, value: UUID):
        self._libraryId = value
    
    @property
    def status(self) -> MetamodelStatus:
        return self._status
    
    @status.setter
    def status(self, value: MetamodelStatus):
        self._status = value
    
    @property
    def storageItemIds(self) -> List[UUID]:
        return self._storageItemIds
    
    @storageItemIds.setter
    def storageItemIds(self, value: List[UUID]):
        self._storageItemIds = value
    
    @property
    def confidenceScore(self) -> Optional[float]:
        return self._confidenceScore
    
    @confidenceScore.setter
    def confidenceScore(self, value: Optional[float]):
        self._confidenceScore = value
    
    @property
    def sellabilityScore(self) -> Optional[float]:
        return self._sellabilityScore
    
    @sellabilityScore.setter
    def sellabilityScore(self, value: Optional[float]):
        self._sellabilityScore = value
    
    @property
    def associatedMediaId(self) -> Optional[UUID]:
        return self._associatedMediaId
    
    @associatedMediaId.setter
    def associatedMediaId(self, value: Optional[UUID]):
        self._associatedMediaId = value
    
    @property
    def internalId(self) -> Optional[str]:
        return self._internalId
    
    @internalId.setter
    def internalId(self, value: Optional[str]):
        self._internalId = value
    
    @property
    def parentMetamodelId(self) -> Optional[UUID]:
        return self._parentMetamodelId
    
    @parentMetamodelId.setter
    def parentMetamodelId(self, value: Optional[UUID]):
        self._parentMetamodelId = value
    
    @property
    def childMetamodelIds(self) -> List[UUID]:
        return self._childMetamodelIds
    
    @childMetamodelIds.setter
    def childMetamodelIds(self, value: List[UUID]):
        self._childMetamodelIds = value
    
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
        if not isinstance(other, MetamodelBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"Metamodel(id={self.id})"
