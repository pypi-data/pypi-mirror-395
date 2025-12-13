"""
Base Aggregate for Model
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from typing import List

from mesh_sync_common.generated.model.processing_error_base import ProcessingErrorBase

from uuid import UUID

from mesh_sync_common.generated.catalog.model_status_base import ModelStatus

from mesh_sync_common.generated.catalog.dimensions_base import DimensionsBase

from mesh_sync_common.generated.model.print_settings_base import PrintSettingsBase

from mesh_sync_common.generated.model.geometry_metrics_base import GeometryMetricsBase

from mesh_sync_common.generated.model.model_dimensions_base import ModelDimensionsBase

from mesh_sync_common.generated.model.quality_metrics_base import QualityMetricsBase

from mesh_sync_common.generated.model.print_estimates_base import PrintEstimatesBase

from mesh_sync_common.generated.model.model_customizations_base import ModelCustomizationsBase

from datetime import datetime


class ModelBase:
    """
    Represents a 3D model asset throughout its lifecycle from discovery to marketplace listing
    """
    
    def __init__(
        self,
        id: UUID,
        
        name: str,
        
        fileName: str,
        
        fileSize: int,
        
        lastProcessingError: ProcessingErrorBase,
        
        ownerId: UUID,
        
        libraryId: UUID,
        
        storageItemId: UUID,
        
        associatedMediaId: UUID,
        
        description: str = None,
        
        generatedDescription: str = None,
        
        status: ModelStatus = None,
        
        fileType: str = None,
        
        dimensions: Optional[DimensionsBase] = None,
        
        printSettings: Optional[PrintSettingsBase] = None,
        
        processing_attempts: int = None,
        
        tagIds: List[UUID] = None,
        
        collectionIds: List[UUID] = None,
        
        marketplaceListingIds: List[UUID] = None,
        
        parentId: Optional[UUID] = None,
        
        level: int = None,
        
        geometry: Optional[GeometryMetricsBase] = None,
        
        physicalDimensions: Optional[ModelDimensionsBase] = None,
        
        quality: Optional[QualityMetricsBase] = None,
        
        printEstimates: Optional[PrintEstimatesBase] = None,
        
        customizations: Optional[ModelCustomizationsBase] = None,
        
        basePrice: float = None,
        
        baseCurrency: str = None,
        
        createdAt: datetime = None,
        
        updatedAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            name=name,
            
            fileName=fileName,
            
            fileSize=fileSize,
            
            lastProcessingError=lastProcessingError,
            
            ownerId=ownerId,
            
            libraryId=libraryId,
            
            storageItemId=storageItemId,
            
            associatedMediaId=associatedMediaId,
            
            description=description,
            
            generatedDescription=generatedDescription,
            
            status=status,
            
            fileType=fileType,
            
            dimensions=dimensions,
            
            printSettings=printSettings,
            
            processing_attempts=processing_attempts,
            
            tagIds=tagIds,
            
            collectionIds=collectionIds,
            
            marketplaceListingIds=marketplaceListingIds,
            
            parentId=parentId,
            
            level=level,
            
            geometry=geometry,
            
            physicalDimensions=physicalDimensions,
            
            quality=quality,
            
            printEstimates=printEstimates,
            
            customizations=customizations,
            
            basePrice=basePrice,
            
            baseCurrency=baseCurrency,
            
            createdAt=createdAt,
            
            updatedAt=updatedAt,
            
        )
        
        self._id = id
        
        self._name = name
        
        self._fileName = fileName
        
        self._fileSize = fileSize
        
        self._lastProcessingError = lastProcessingError
        
        self._ownerId = ownerId
        
        self._libraryId = libraryId
        
        self._storageItemId = storageItemId
        
        self._associatedMediaId = associatedMediaId
        
        self._description = description
        
        self._generatedDescription = generatedDescription
        
        self._status = status
        
        self._fileType = fileType
        
        self._dimensions = dimensions
        
        self._printSettings = printSettings
        
        self._processing_attempts = processing_attempts
        
        self._tagIds = tagIds
        
        self._collectionIds = collectionIds
        
        self._marketplaceListingIds = marketplaceListingIds
        
        self._parentId = parentId
        
        self._level = level
        
        self._geometry = geometry
        
        self._physicalDimensions = physicalDimensions
        
        self._quality = quality
        
        self._printEstimates = printEstimates
        
        self._customizations = customizations
        
        self._basePrice = basePrice
        
        self._baseCurrency = baseCurrency
        
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
        
        
        
        
        
        
        # fileName: required field
        if kwargs.get('fileName') is None:
            errors.append('fileName is required')
        
        
        
        
        
        
        # fileSize: required field
        if kwargs.get('fileSize') is None:
            errors.append('fileSize is required')
        
        
        # fileSize: min constraint
        if kwargs.get('fileSize') is not None and kwargs.get('fileSize') < 0:
            errors.append('fileSize must be >= 0')
        
        
        
        
        
        # lastProcessingError: required field
        if kwargs.get('lastProcessingError') is None:
            errors.append('lastProcessingError is required')
        
        
        
        
        
        
        # ownerId: required field
        if kwargs.get('ownerId') is None:
            errors.append('ownerId is required')
        
        
        
        
        
        
        # libraryId: required field
        if kwargs.get('libraryId') is None:
            errors.append('libraryId is required')
        
        
        
        
        
        
        # storageItemId: required field
        if kwargs.get('storageItemId') is None:
            errors.append('storageItemId is required')
        
        
        
        
        
        
        # associatedMediaId: required field
        if kwargs.get('associatedMediaId') is None:
            errors.append('associatedMediaId is required')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # processing_attempts: min constraint
        if kwargs.get('processing_attempts') is not None and kwargs.get('processing_attempts') < 0:
            errors.append('processing_attempts must be >= 0')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # level: min constraint
        if kwargs.get('level') is not None and kwargs.get('level') < 0:
            errors.append('level must be >= 0')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # basePrice: min constraint
        if kwargs.get('basePrice') is not None and kwargs.get('basePrice') < 0:
            errors.append('basePrice must be >= 0')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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
    def fileName(self) -> str:
        return self._fileName
    
    @fileName.setter
    def fileName(self, value: str):
        self._fileName = value
    
    @property
    def fileSize(self) -> int:
        return self._fileSize
    
    @fileSize.setter
    def fileSize(self, value: int):
        self._fileSize = value
    
    @property
    def lastProcessingError(self) -> ProcessingErrorBase:
        return self._lastProcessingError
    
    @lastProcessingError.setter
    def lastProcessingError(self, value: ProcessingErrorBase):
        self._lastProcessingError = value
    
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
    def storageItemId(self) -> UUID:
        return self._storageItemId
    
    @storageItemId.setter
    def storageItemId(self, value: UUID):
        self._storageItemId = value
    
    @property
    def associatedMediaId(self) -> UUID:
        return self._associatedMediaId
    
    @associatedMediaId.setter
    def associatedMediaId(self, value: UUID):
        self._associatedMediaId = value
    
    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str):
        self._description = value
    
    @property
    def generatedDescription(self) -> str:
        return self._generatedDescription
    
    @generatedDescription.setter
    def generatedDescription(self, value: str):
        self._generatedDescription = value
    
    @property
    def status(self) -> ModelStatus:
        return self._status
    
    @status.setter
    def status(self, value: ModelStatus):
        self._status = value
    
    @property
    def fileType(self) -> str:
        return self._fileType
    
    @fileType.setter
    def fileType(self, value: str):
        self._fileType = value
    
    @property
    def dimensions(self) -> Optional[DimensionsBase]:
        return self._dimensions
    
    @dimensions.setter
    def dimensions(self, value: Optional[DimensionsBase]):
        self._dimensions = value
    
    @property
    def printSettings(self) -> Optional[PrintSettingsBase]:
        return self._printSettings
    
    @printSettings.setter
    def printSettings(self, value: Optional[PrintSettingsBase]):
        self._printSettings = value
    
    @property
    def processing_attempts(self) -> int:
        return self._processing_attempts
    
    @processing_attempts.setter
    def processing_attempts(self, value: int):
        self._processing_attempts = value
    
    @property
    def tagIds(self) -> List[UUID]:
        return self._tagIds
    
    @tagIds.setter
    def tagIds(self, value: List[UUID]):
        self._tagIds = value
    
    @property
    def collectionIds(self) -> List[UUID]:
        return self._collectionIds
    
    @collectionIds.setter
    def collectionIds(self, value: List[UUID]):
        self._collectionIds = value
    
    @property
    def marketplaceListingIds(self) -> List[UUID]:
        return self._marketplaceListingIds
    
    @marketplaceListingIds.setter
    def marketplaceListingIds(self, value: List[UUID]):
        self._marketplaceListingIds = value
    
    @property
    def parentId(self) -> Optional[UUID]:
        return self._parentId
    
    @parentId.setter
    def parentId(self, value: Optional[UUID]):
        self._parentId = value
    
    @property
    def level(self) -> int:
        return self._level
    
    @level.setter
    def level(self, value: int):
        self._level = value
    
    @property
    def geometry(self) -> Optional[GeometryMetricsBase]:
        return self._geometry
    
    @geometry.setter
    def geometry(self, value: Optional[GeometryMetricsBase]):
        self._geometry = value
    
    @property
    def physicalDimensions(self) -> Optional[ModelDimensionsBase]:
        return self._physicalDimensions
    
    @physicalDimensions.setter
    def physicalDimensions(self, value: Optional[ModelDimensionsBase]):
        self._physicalDimensions = value
    
    @property
    def quality(self) -> Optional[QualityMetricsBase]:
        return self._quality
    
    @quality.setter
    def quality(self, value: Optional[QualityMetricsBase]):
        self._quality = value
    
    @property
    def printEstimates(self) -> Optional[PrintEstimatesBase]:
        return self._printEstimates
    
    @printEstimates.setter
    def printEstimates(self, value: Optional[PrintEstimatesBase]):
        self._printEstimates = value
    
    @property
    def customizations(self) -> Optional[ModelCustomizationsBase]:
        return self._customizations
    
    @customizations.setter
    def customizations(self, value: Optional[ModelCustomizationsBase]):
        self._customizations = value
    
    @property
    def basePrice(self) -> float:
        return self._basePrice
    
    @basePrice.setter
    def basePrice(self, value: float):
        self._basePrice = value
    
    @property
    def baseCurrency(self) -> str:
        return self._baseCurrency
    
    @baseCurrency.setter
    def baseCurrency(self, value: str):
        self._baseCurrency = value
    
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
        if not isinstance(other, ModelBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"Model(id={self.id})"
