"""
Base Aggregate for Notification
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from uuid import UUID

from mesh_sync_common.generated.notifications.notification_type_base import NotificationType

from mesh_sync_common.generated.notifications.notification_priority_base import NotificationPriority

from datetime import datetime


class NotificationBase:
    """
    Represents a system notification for a user
    """
    
    def __init__(
        self,
        id: UUID,
        
        userId: UUID,
        
        type: NotificationType,
        
        title: str,
        
        message: str,
        
        priority: NotificationPriority = None,
        
        entityId: Optional[str] = None,
        
        entityType: Optional[str] = None,
        
        actionUrl: Optional[str] = None,
        
        metadata: Any = None,
        
        isRead: bool = None,
        
        readAt: Optional[datetime] = None,
        
        createdAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            userId=userId,
            
            type=type,
            
            title=title,
            
            message=message,
            
            priority=priority,
            
            entityId=entityId,
            
            entityType=entityType,
            
            actionUrl=actionUrl,
            
            metadata=metadata,
            
            isRead=isRead,
            
            readAt=readAt,
            
            createdAt=createdAt,
            
        )
        
        self._id = id
        
        self._userId = userId
        
        self._type = type
        
        self._title = title
        
        self._message = message
        
        self._priority = priority
        
        self._entityId = entityId
        
        self._entityType = entityType
        
        self._actionUrl = actionUrl
        
        self._metadata = metadata
        
        self._isRead = isRead
        
        self._readAt = readAt
        
        self._createdAt = createdAt
        

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
        
        
        
        
        
        
        # title: required field
        if kwargs.get('title') is None:
            errors.append('title is required')
        
        
        
        
        
        
        # message: required field
        if kwargs.get('message') is None:
            errors.append('message is required')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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
    def type(self) -> NotificationType:
        return self._type
    
    @type.setter
    def type(self, value: NotificationType):
        self._type = value
    
    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, value: str):
        self._title = value
    
    @property
    def message(self) -> str:
        return self._message
    
    @message.setter
    def message(self, value: str):
        self._message = value
    
    @property
    def priority(self) -> NotificationPriority:
        return self._priority
    
    @priority.setter
    def priority(self, value: NotificationPriority):
        self._priority = value
    
    @property
    def entityId(self) -> Optional[str]:
        return self._entityId
    
    @entityId.setter
    def entityId(self, value: Optional[str]):
        self._entityId = value
    
    @property
    def entityType(self) -> Optional[str]:
        return self._entityType
    
    @entityType.setter
    def entityType(self, value: Optional[str]):
        self._entityType = value
    
    @property
    def actionUrl(self) -> Optional[str]:
        return self._actionUrl
    
    @actionUrl.setter
    def actionUrl(self, value: Optional[str]):
        self._actionUrl = value
    
    @property
    def metadata(self) -> Any:
        return self._metadata
    
    @metadata.setter
    def metadata(self, value: Any):
        self._metadata = value
    
    @property
    def isRead(self) -> bool:
        return self._isRead
    
    @isRead.setter
    def isRead(self, value: bool):
        self._isRead = value
    
    @property
    def readAt(self) -> Optional[datetime]:
        return self._readAt
    
    @readAt.setter
    def readAt(self, value: Optional[datetime]):
        self._readAt = value
    
    @property
    def createdAt(self) -> datetime:
        return self._createdAt
    
    @createdAt.setter
    def createdAt(self, value: datetime):
        self._createdAt = value
    

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, NotificationBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"Notification(id={self.id})"
