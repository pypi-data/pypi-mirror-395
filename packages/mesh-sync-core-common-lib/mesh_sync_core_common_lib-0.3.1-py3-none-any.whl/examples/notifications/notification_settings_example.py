"""
Example usage for NotificationSettings
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.notifications.notification_settings import NotificationSettings

def example_notification_settings():
    print("Creating NotificationSettings...")
    
    instance = NotificationSettings(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        userId=None,
        
        emailEnabled=True,
        
        pushEnabled=True,
        
        inAppEnabled=True,
        
        enabledTypes=None,
        
        quietHoursStart=None,
        
        quietHoursEnd=None,
        
        frequency=None,
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_notification_settings()
