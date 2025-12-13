"""
Base Aggregate for Model
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from uuid import UUID

from datetime import datetime

from mesh_sync_common.generated.catalog.model_status_base import ModelStatus

from mesh_sync_common.generated.catalog.dimensions_base import DimensionsBase


class ModelBase:
    """
    Represents a 3D model asset in the system
    """
    
    def __init__(
        self,
        ModelId: UUID,
        
        name: str,
        
        fileName: str,
        
        fileSize: float,
        
        ownerId: UUID,
        
        libraryId: UUID,
        
        createdAt: datetime,
        
        updatedAt: datetime,
        
        status: ModelStatus = None,
        
        dimensions: Optional[DimensionsBase] = None,
        
    ):
        # Validate all fields
        self._validate(
            ModelId=ModelId,
            
            name=name,
            
            fileName=fileName,
            
            fileSize=fileSize,
            
            ownerId=ownerId,
            
            libraryId=libraryId,
            
            createdAt=createdAt,
            
            updatedAt=updatedAt,
            
            status=status,
            
            dimensions=dimensions,
            
        )
        
        self._ModelId = ModelId
        
        self._name = name
        
        self._fileName = fileName
        
        self._fileSize = fileSize
        
        self._ownerId = ownerId
        
        self._libraryId = libraryId
        
        self._createdAt = createdAt
        
        self._updatedAt = updatedAt
        
        self._status = status
        
        self._dimensions = dimensions
        

    def _validate(self, **kwargs) -> None:
        """Validate all required fields and constraints"""
        errors = []
        
        # Identity validation
        if kwargs.get('ModelId') is None:
            errors.append('ModelId is required')
        
        
        
        # name: required field
        if kwargs.get('name') is None:
            errors.append('name is required')
        
        
        
        
        
        
        # fileName: required field
        if kwargs.get('fileName') is None:
            errors.append('fileName is required')
        
        
        
        
        
        
        # fileSize: required field
        if kwargs.get('fileSize') is None:
            errors.append('fileSize is required')
        
        
        # fileSize: min constraint
        if kwargs.get('fileSize') is not None and kwargs.get('fileSize') < 0:
            errors.append('fileSize must be >= 0')
        
        
        
        
        
        # ownerId: required field
        if kwargs.get('ownerId') is None:
            errors.append('ownerId is required')
        
        
        
        
        
        
        # libraryId: required field
        if kwargs.get('libraryId') is None:
            errors.append('libraryId is required')
        
        
        
        
        
        
        # createdAt: required field
        if kwargs.get('createdAt') is None:
            errors.append('createdAt is required')
        
        
        
        
        
        
        # updatedAt: required field
        if kwargs.get('updatedAt') is None:
            errors.append('updatedAt is required')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if errors:
            raise ValueError('; '.join(errors))

    @property
    def ModelId(self) -> UUID:
        return self._ModelId

    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        self._name = value
    
    @property
    def fileName(self) -> str:
        return self._fileName
    
    @fileName.setter
    def fileName(self, value: str):
        self._fileName = value
    
    @property
    def fileSize(self) -> float:
        return self._fileSize
    
    @fileSize.setter
    def fileSize(self, value: float):
        self._fileSize = value
    
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
    
    @property
    def status(self) -> ModelStatus:
        return self._status
    
    @status.setter
    def status(self, value: ModelStatus):
        self._status = value
    
    @property
    def dimensions(self) -> Optional[DimensionsBase]:
        return self._dimensions
    
    @dimensions.setter
    def dimensions(self, value: Optional[DimensionsBase]):
        self._dimensions = value
    

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ModelBase):
            return False
        return self.ModelId == other.ModelId

    def __hash__(self) -> int:
        return hash(self.ModelId)

    def __repr__(self) -> str:
        return f"Model(ModelId={self.ModelId})"
