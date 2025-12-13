"""
Base Aggregate for ThumbnailMedia
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from mesh_sync_common.generated.media.media_type_base import MediaType

from mesh_sync_common.generated.media.watermark_base import WatermarkBase

from datetime import datetime


class ThumbnailMediaBase:
    """
    Represents a single media file (image, video, or 3D thumbnail)
    """
    
    def __init__(
        self,
        id: UUID,
        
        mediaType: MediaType,
        
        storagePath: str,
        
        originalFileName: str,
        
        mimeType: str,
        
        fileSize: int,
        
        watermark: Optional[WatermarkBase] = None,
        
        width: Optional[int] = None,
        
        height: Optional[int] = None,
        
        duration: Optional[float] = None,
        
        createdAt: datetime = None,
        
        updatedAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            mediaType=mediaType,
            
            storagePath=storagePath,
            
            originalFileName=originalFileName,
            
            mimeType=mimeType,
            
            fileSize=fileSize,
            
            watermark=watermark,
            
            width=width,
            
            height=height,
            
            duration=duration,
            
            createdAt=createdAt,
            
            updatedAt=updatedAt,
            
        )
        
        self._id = id
        
        self._mediaType = mediaType
        
        self._storagePath = storagePath
        
        self._originalFileName = originalFileName
        
        self._mimeType = mimeType
        
        self._fileSize = fileSize
        
        self._watermark = watermark
        
        self._width = width
        
        self._height = height
        
        self._duration = duration
        
        self._createdAt = createdAt
        
        self._updatedAt = updatedAt
        

    def _validate(self, **kwargs) -> None:
        """Validate all required fields and constraints"""
        errors = []
        
        # Identity validation
        if kwargs.get('id') is None:
            errors.append('id is required')
        
        
        
        # mediaType: required field
        if kwargs.get('mediaType') is None:
            errors.append('mediaType is required')
        
        
        
        
        
        
        # storagePath: required field
        if kwargs.get('storagePath') is None:
            errors.append('storagePath is required')
        
        
        
        
        
        
        # originalFileName: required field
        if kwargs.get('originalFileName') is None:
            errors.append('originalFileName is required')
        
        
        
        
        
        
        # mimeType: required field
        if kwargs.get('mimeType') is None:
            errors.append('mimeType is required')
        
        
        
        
        
        
        # fileSize: required field
        if kwargs.get('fileSize') is None:
            errors.append('fileSize is required')
        
        
        # fileSize: min constraint
        if kwargs.get('fileSize') is not None and kwargs.get('fileSize') < 0:
            errors.append('fileSize must be >= 0')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if errors:
            raise ValueError('; '.join(errors))

    @property
    def id(self) -> UUID:
        return self._id

    
    @property
    def mediaType(self) -> MediaType:
        return self._mediaType
    
    @mediaType.setter
    def mediaType(self, value: MediaType):
        self._mediaType = value
    
    @property
    def storagePath(self) -> str:
        return self._storagePath
    
    @storagePath.setter
    def storagePath(self, value: str):
        self._storagePath = value
    
    @property
    def originalFileName(self) -> str:
        return self._originalFileName
    
    @originalFileName.setter
    def originalFileName(self, value: str):
        self._originalFileName = value
    
    @property
    def mimeType(self) -> str:
        return self._mimeType
    
    @mimeType.setter
    def mimeType(self, value: str):
        self._mimeType = value
    
    @property
    def fileSize(self) -> int:
        return self._fileSize
    
    @fileSize.setter
    def fileSize(self, value: int):
        self._fileSize = value
    
    @property
    def watermark(self) -> Optional[WatermarkBase]:
        return self._watermark
    
    @watermark.setter
    def watermark(self, value: Optional[WatermarkBase]):
        self._watermark = value
    
    @property
    def width(self) -> Optional[int]:
        return self._width
    
    @width.setter
    def width(self, value: Optional[int]):
        self._width = value
    
    @property
    def height(self) -> Optional[int]:
        return self._height
    
    @height.setter
    def height(self, value: Optional[int]):
        self._height = value
    
    @property
    def duration(self) -> Optional[float]:
        return self._duration
    
    @duration.setter
    def duration(self, value: Optional[float]):
        self._duration = value
    
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
        if not isinstance(other, ThumbnailMediaBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"ThumbnailMedia(id={self.id})"
