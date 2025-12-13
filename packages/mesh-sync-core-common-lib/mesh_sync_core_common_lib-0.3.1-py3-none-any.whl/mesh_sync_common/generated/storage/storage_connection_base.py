"""
Base Aggregate for StorageConnection
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from uuid import UUID

from mesh_sync_common.generated.storage.storage_provider_type_base import StorageProviderType

from mesh_sync_common.generated.storage.scan_status_base import ScanStatus

from datetime import datetime


class StorageConnectionBase:
    """
    Represents a connection to a storage provider for scanning and syncing files
    """
    
    def __init__(
        self,
        id: UUID,
        
        storageProviderConfigId: UUID,
        
        name: str,
        
        providerType: StorageProviderType,
        
        userId: Optional[UUID] = None,
        
        libraryId: Optional[UUID] = None,
        
        rootPath: Optional[str] = None,
        
        isActive: bool = None,
        
        lastScanStatus: ScanStatus = None,
        
        lastScanError: Optional[str] = None,
        
        lastScanAt: Optional[datetime] = None,
        
        encryptedCredentials: Optional[str] = None,
        
        createdAt: datetime = None,
        
        updatedAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            storageProviderConfigId=storageProviderConfigId,
            
            name=name,
            
            providerType=providerType,
            
            userId=userId,
            
            libraryId=libraryId,
            
            rootPath=rootPath,
            
            isActive=isActive,
            
            lastScanStatus=lastScanStatus,
            
            lastScanError=lastScanError,
            
            lastScanAt=lastScanAt,
            
            encryptedCredentials=encryptedCredentials,
            
            createdAt=createdAt,
            
            updatedAt=updatedAt,
            
        )
        
        self._id = id
        
        self._storageProviderConfigId = storageProviderConfigId
        
        self._name = name
        
        self._providerType = providerType
        
        self._userId = userId
        
        self._libraryId = libraryId
        
        self._rootPath = rootPath
        
        self._isActive = isActive
        
        self._lastScanStatus = lastScanStatus
        
        self._lastScanError = lastScanError
        
        self._lastScanAt = lastScanAt
        
        self._encryptedCredentials = encryptedCredentials
        
        self._createdAt = createdAt
        
        self._updatedAt = updatedAt
        

    def _validate(self, **kwargs) -> None:
        """Validate all required fields and constraints"""
        errors = []
        
        # Identity validation
        if kwargs.get('id') is None:
            errors.append('id is required')
        
        
        
        # storageProviderConfigId: required field
        if kwargs.get('storageProviderConfigId') is None:
            errors.append('storageProviderConfigId is required')
        
        
        
        
        
        
        # name: required field
        if kwargs.get('name') is None:
            errors.append('name is required')
        
        
        
        
        
        
        # providerType: required field
        if kwargs.get('providerType') is None:
            errors.append('providerType is required')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if errors:
            raise ValueError('; '.join(errors))

    @property
    def id(self) -> UUID:
        return self._id

    
    @property
    def storageProviderConfigId(self) -> UUID:
        return self._storageProviderConfigId
    
    @storageProviderConfigId.setter
    def storageProviderConfigId(self, value: UUID):
        self._storageProviderConfigId = value
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        self._name = value
    
    @property
    def providerType(self) -> StorageProviderType:
        return self._providerType
    
    @providerType.setter
    def providerType(self, value: StorageProviderType):
        self._providerType = value
    
    @property
    def userId(self) -> Optional[UUID]:
        return self._userId
    
    @userId.setter
    def userId(self, value: Optional[UUID]):
        self._userId = value
    
    @property
    def libraryId(self) -> Optional[UUID]:
        return self._libraryId
    
    @libraryId.setter
    def libraryId(self, value: Optional[UUID]):
        self._libraryId = value
    
    @property
    def rootPath(self) -> Optional[str]:
        return self._rootPath
    
    @rootPath.setter
    def rootPath(self, value: Optional[str]):
        self._rootPath = value
    
    @property
    def isActive(self) -> bool:
        return self._isActive
    
    @isActive.setter
    def isActive(self, value: bool):
        self._isActive = value
    
    @property
    def lastScanStatus(self) -> ScanStatus:
        return self._lastScanStatus
    
    @lastScanStatus.setter
    def lastScanStatus(self, value: ScanStatus):
        self._lastScanStatus = value
    
    @property
    def lastScanError(self) -> Optional[str]:
        return self._lastScanError
    
    @lastScanError.setter
    def lastScanError(self, value: Optional[str]):
        self._lastScanError = value
    
    @property
    def lastScanAt(self) -> Optional[datetime]:
        return self._lastScanAt
    
    @lastScanAt.setter
    def lastScanAt(self, value: Optional[datetime]):
        self._lastScanAt = value
    
    @property
    def encryptedCredentials(self) -> Optional[str]:
        return self._encryptedCredentials
    
    @encryptedCredentials.setter
    def encryptedCredentials(self, value: Optional[str]):
        self._encryptedCredentials = value
    
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
        if not isinstance(other, StorageConnectionBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"StorageConnection(id={self.id})"
