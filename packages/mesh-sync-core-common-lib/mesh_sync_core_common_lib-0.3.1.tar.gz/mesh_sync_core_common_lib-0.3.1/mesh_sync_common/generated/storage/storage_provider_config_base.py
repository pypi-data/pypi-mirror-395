"""
Base Aggregate for StorageProviderConfig
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from uuid import UUID

from mesh_sync_common.generated.storage.storage_provider_type_base import StorageProviderType

from mesh_sync_common.generated.storage.provider_configuration_base import ProviderConfigurationBase

from mesh_sync_common.generated.storage.provider_credentials_base import ProviderCredentialsBase

from datetime import datetime

from mesh_sync_common.generated.storage.model_identification_rules_base import ModelIdentificationRulesBase


class StorageProviderConfigBase:
    """
    Configuration for a specific instance of a storage provider connection
    """
    
    def __init__(
        self,
        id: UUID,
        
        userId: UUID,
        
        name: str,
        
        type: StorageProviderType,
        
        scanRootPath: str,
        
        configuration: ProviderConfigurationBase,
        
        encryptedCredentials: ProviderCredentialsBase,
        
        maxScanDepth: int = None,
        
        isConnected: bool = None,
        
        lastConnectionAttempt: Optional[datetime] = None,
        
        lastConnectionError: Optional[str] = None,
        
        lastScanAt: Optional[datetime] = None,
        
        modelIdentificationRules: Optional[ModelIdentificationRulesBase] = None,
        
        createdAt: datetime = None,
        
        updatedAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            userId=userId,
            
            name=name,
            
            type=type,
            
            scanRootPath=scanRootPath,
            
            configuration=configuration,
            
            encryptedCredentials=encryptedCredentials,
            
            maxScanDepth=maxScanDepth,
            
            isConnected=isConnected,
            
            lastConnectionAttempt=lastConnectionAttempt,
            
            lastConnectionError=lastConnectionError,
            
            lastScanAt=lastScanAt,
            
            modelIdentificationRules=modelIdentificationRules,
            
            createdAt=createdAt,
            
            updatedAt=updatedAt,
            
        )
        
        self._id = id
        
        self._userId = userId
        
        self._name = name
        
        self._type = type
        
        self._scanRootPath = scanRootPath
        
        self._configuration = configuration
        
        self._encryptedCredentials = encryptedCredentials
        
        self._maxScanDepth = maxScanDepth
        
        self._isConnected = isConnected
        
        self._lastConnectionAttempt = lastConnectionAttempt
        
        self._lastConnectionError = lastConnectionError
        
        self._lastScanAt = lastScanAt
        
        self._modelIdentificationRules = modelIdentificationRules
        
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
        
        
        
        
        
        
        # scanRootPath: required field
        if kwargs.get('scanRootPath') is None:
            errors.append('scanRootPath is required')
        
        
        
        
        
        
        # configuration: required field
        if kwargs.get('configuration') is None:
            errors.append('configuration is required')
        
        
        
        
        
        
        # encryptedCredentials: required field
        if kwargs.get('encryptedCredentials') is None:
            errors.append('encryptedCredentials is required')
        
        
        
        
        
        
        
        # maxScanDepth: min constraint
        if kwargs.get('maxScanDepth') is not None and kwargs.get('maxScanDepth') < 1:
            errors.append('maxScanDepth must be >= 1')
        
        
        # maxScanDepth: max constraint
        if kwargs.get('maxScanDepth') is not None and kwargs.get('maxScanDepth') > 50:
            errors.append('maxScanDepth must be <= 50')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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
    def type(self) -> StorageProviderType:
        return self._type
    
    @type.setter
    def type(self, value: StorageProviderType):
        self._type = value
    
    @property
    def scanRootPath(self) -> str:
        return self._scanRootPath
    
    @scanRootPath.setter
    def scanRootPath(self, value: str):
        self._scanRootPath = value
    
    @property
    def configuration(self) -> ProviderConfigurationBase:
        return self._configuration
    
    @configuration.setter
    def configuration(self, value: ProviderConfigurationBase):
        self._configuration = value
    
    @property
    def encryptedCredentials(self) -> ProviderCredentialsBase:
        return self._encryptedCredentials
    
    @encryptedCredentials.setter
    def encryptedCredentials(self, value: ProviderCredentialsBase):
        self._encryptedCredentials = value
    
    @property
    def maxScanDepth(self) -> int:
        return self._maxScanDepth
    
    @maxScanDepth.setter
    def maxScanDepth(self, value: int):
        self._maxScanDepth = value
    
    @property
    def isConnected(self) -> bool:
        return self._isConnected
    
    @isConnected.setter
    def isConnected(self, value: bool):
        self._isConnected = value
    
    @property
    def lastConnectionAttempt(self) -> Optional[datetime]:
        return self._lastConnectionAttempt
    
    @lastConnectionAttempt.setter
    def lastConnectionAttempt(self, value: Optional[datetime]):
        self._lastConnectionAttempt = value
    
    @property
    def lastConnectionError(self) -> Optional[str]:
        return self._lastConnectionError
    
    @lastConnectionError.setter
    def lastConnectionError(self, value: Optional[str]):
        self._lastConnectionError = value
    
    @property
    def lastScanAt(self) -> Optional[datetime]:
        return self._lastScanAt
    
    @lastScanAt.setter
    def lastScanAt(self, value: Optional[datetime]):
        self._lastScanAt = value
    
    @property
    def modelIdentificationRules(self) -> Optional[ModelIdentificationRulesBase]:
        return self._modelIdentificationRules
    
    @modelIdentificationRules.setter
    def modelIdentificationRules(self, value: Optional[ModelIdentificationRulesBase]):
        self._modelIdentificationRules = value
    
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
        if not isinstance(other, StorageProviderConfigBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"StorageProviderConfig(id={self.id})"
