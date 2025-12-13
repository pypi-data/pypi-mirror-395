"""
Base Aggregate for NotificationSettings
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from typing import List

from uuid import UUID

from mesh_sync_common.generated.notifications.notification_frequency_base import NotificationFrequency


class NotificationSettingsBase:
    """
    User preferences for notifications
    """
    
    def __init__(
        self,
        id: UUID,
        
        userId: UUID,
        
        emailEnabled: bool = None,
        
        pushEnabled: bool = None,
        
        inAppEnabled: bool = None,
        
        enabledTypes: List[str] = None,
        
        quietHoursStart: Optional[str] = None,
        
        quietHoursEnd: Optional[str] = None,
        
        frequency: NotificationFrequency = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            userId=userId,
            
            emailEnabled=emailEnabled,
            
            pushEnabled=pushEnabled,
            
            inAppEnabled=inAppEnabled,
            
            enabledTypes=enabledTypes,
            
            quietHoursStart=quietHoursStart,
            
            quietHoursEnd=quietHoursEnd,
            
            frequency=frequency,
            
        )
        
        self._id = id
        
        self._userId = userId
        
        self._emailEnabled = emailEnabled
        
        self._pushEnabled = pushEnabled
        
        self._inAppEnabled = inAppEnabled
        
        self._enabledTypes = enabledTypes
        
        self._quietHoursStart = quietHoursStart
        
        self._quietHoursEnd = quietHoursEnd
        
        self._frequency = frequency
        

    def _validate(self, **kwargs) -> None:
        """Validate all required fields and constraints"""
        errors = []
        
        # Identity validation
        if kwargs.get('id') is None:
            errors.append('id is required')
        
        
        
        # userId: required field
        if kwargs.get('userId') is None:
            errors.append('userId is required')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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
    def emailEnabled(self) -> bool:
        return self._emailEnabled
    
    @emailEnabled.setter
    def emailEnabled(self, value: bool):
        self._emailEnabled = value
    
    @property
    def pushEnabled(self) -> bool:
        return self._pushEnabled
    
    @pushEnabled.setter
    def pushEnabled(self, value: bool):
        self._pushEnabled = value
    
    @property
    def inAppEnabled(self) -> bool:
        return self._inAppEnabled
    
    @inAppEnabled.setter
    def inAppEnabled(self, value: bool):
        self._inAppEnabled = value
    
    @property
    def enabledTypes(self) -> List[str]:
        return self._enabledTypes
    
    @enabledTypes.setter
    def enabledTypes(self, value: List[str]):
        self._enabledTypes = value
    
    @property
    def quietHoursStart(self) -> Optional[str]:
        return self._quietHoursStart
    
    @quietHoursStart.setter
    def quietHoursStart(self, value: Optional[str]):
        self._quietHoursStart = value
    
    @property
    def quietHoursEnd(self) -> Optional[str]:
        return self._quietHoursEnd
    
    @quietHoursEnd.setter
    def quietHoursEnd(self, value: Optional[str]):
        self._quietHoursEnd = value
    
    @property
    def frequency(self) -> NotificationFrequency:
        return self._frequency
    
    @frequency.setter
    def frequency(self, value: NotificationFrequency):
        self._frequency = value
    

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, NotificationSettingsBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"NotificationSettings(id={self.id})"
