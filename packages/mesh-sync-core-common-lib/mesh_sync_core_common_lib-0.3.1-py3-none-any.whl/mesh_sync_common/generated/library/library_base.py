"""
Base Aggregate for Library
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from mesh_sync_common.generated.library.validation_result_base import ValidationResultBase

from uuid import UUID

from mesh_sync_common.generated.library.library_stats_base import LibraryStatsBase

from mesh_sync_common.generated.library.library_scan_status_base import LibraryScanStatus

from datetime import datetime


class LibraryBase:
    """
    Represents a library of 3D models from a specific storage location
    """
    
    def __init__(
        self,
        id: UUID,
        
        name: str,
        
        path: str,
        
        validationResult: ValidationResultBase,
        
        storageProviderConfigId: UUID,
        
        stats: LibraryStatsBase,
        
        userId: UUID,
        
        scanStatus: LibraryScanStatus = None,
        
        lastScanTime: Optional[datetime] = None,
        
        createdAt: datetime = None,
        
        updatedAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            name=name,
            
            path=path,
            
            validationResult=validationResult,
            
            storageProviderConfigId=storageProviderConfigId,
            
            stats=stats,
            
            userId=userId,
            
            scanStatus=scanStatus,
            
            lastScanTime=lastScanTime,
            
            createdAt=createdAt,
            
            updatedAt=updatedAt,
            
        )
        
        self._id = id
        
        self._name = name
        
        self._path = path
        
        self._validationResult = validationResult
        
        self._storageProviderConfigId = storageProviderConfigId
        
        self._stats = stats
        
        self._userId = userId
        
        self._scanStatus = scanStatus
        
        self._lastScanTime = lastScanTime
        
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
        
        
        
        
        
        
        # path: required field
        if kwargs.get('path') is None:
            errors.append('path is required')
        
        
        
        
        
        
        # validationResult: required field
        if kwargs.get('validationResult') is None:
            errors.append('validationResult is required')
        
        
        
        
        
        
        # storageProviderConfigId: required field
        if kwargs.get('storageProviderConfigId') is None:
            errors.append('storageProviderConfigId is required')
        
        
        
        
        
        
        # stats: required field
        if kwargs.get('stats') is None:
            errors.append('stats is required')
        
        
        
        
        
        
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
    def path(self) -> str:
        return self._path
    
    @path.setter
    def path(self, value: str):
        self._path = value
    
    @property
    def validationResult(self) -> ValidationResultBase:
        return self._validationResult
    
    @validationResult.setter
    def validationResult(self, value: ValidationResultBase):
        self._validationResult = value
    
    @property
    def storageProviderConfigId(self) -> UUID:
        return self._storageProviderConfigId
    
    @storageProviderConfigId.setter
    def storageProviderConfigId(self, value: UUID):
        self._storageProviderConfigId = value
    
    @property
    def stats(self) -> LibraryStatsBase:
        return self._stats
    
    @stats.setter
    def stats(self, value: LibraryStatsBase):
        self._stats = value
    
    @property
    def userId(self) -> UUID:
        return self._userId
    
    @userId.setter
    def userId(self, value: UUID):
        self._userId = value
    
    @property
    def scanStatus(self) -> LibraryScanStatus:
        return self._scanStatus
    
    @scanStatus.setter
    def scanStatus(self, value: LibraryScanStatus):
        self._scanStatus = value
    
    @property
    def lastScanTime(self) -> Optional[datetime]:
        return self._lastScanTime
    
    @lastScanTime.setter
    def lastScanTime(self, value: Optional[datetime]):
        self._lastScanTime = value
    
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
        if not isinstance(other, LibraryBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"Library(id={self.id})"
