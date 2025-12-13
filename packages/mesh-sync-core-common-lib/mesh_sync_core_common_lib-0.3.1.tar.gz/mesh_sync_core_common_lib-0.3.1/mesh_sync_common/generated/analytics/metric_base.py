"""
Base Aggregate for Metric
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from uuid import UUID

from mesh_sync_common.generated.analytics.metric_type_base import MetricType

from datetime import datetime


class MetricBase:
    """
    Represents a single analytic event or metric
    """
    
    def __init__(
        self,
        id: UUID,
        
        userId: UUID,
        
        type: MetricType,
        
        entityId: str,
        
        entityType: str,
        
        value: float = None,
        
        metadata: Any = None,
        
        recordedAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            userId=userId,
            
            type=type,
            
            entityId=entityId,
            
            entityType=entityType,
            
            value=value,
            
            metadata=metadata,
            
            recordedAt=recordedAt,
            
        )
        
        self._id = id
        
        self._userId = userId
        
        self._type = type
        
        self._entityId = entityId
        
        self._entityType = entityType
        
        self._value = value
        
        self._metadata = metadata
        
        self._recordedAt = recordedAt
        

    def _validate(self, **kwargs) -> None:
        """Validate all required fields and constraints"""
        errors = []
        
        # Identity validation
        if kwargs.get('id') is None:
            errors.append('id is required')
        
        
        
        # userId: required field
        if kwargs.get('userId') is None:
            errors.append('userId is required')
        
        
        
        
        
        
        # type: required field
        if kwargs.get('type') is None:
            errors.append('type is required')
        
        
        
        
        
        
        # entityId: required field
        if kwargs.get('entityId') is None:
            errors.append('entityId is required')
        
        
        
        
        
        
        # entityType: required field
        if kwargs.get('entityType') is None:
            errors.append('entityType is required')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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
    def type(self) -> MetricType:
        return self._type
    
    @type.setter
    def type(self, value: MetricType):
        self._type = value
    
    @property
    def entityId(self) -> str:
        return self._entityId
    
    @entityId.setter
    def entityId(self, value: str):
        self._entityId = value
    
    @property
    def entityType(self) -> str:
        return self._entityType
    
    @entityType.setter
    def entityType(self, value: str):
        self._entityType = value
    
    @property
    def value(self) -> float:
        return self._value
    
    @value.setter
    def value(self, value: float):
        self._value = value
    
    @property
    def metadata(self) -> Any:
        return self._metadata
    
    @metadata.setter
    def metadata(self, value: Any):
        self._metadata = value
    
    @property
    def recordedAt(self) -> datetime:
        return self._recordedAt
    
    @recordedAt.setter
    def recordedAt(self, value: datetime):
        self._recordedAt = value
    

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MetricBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"Metric(id={self.id})"
