"""
Example usage for Notification
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.notifications.notification import Notification

def example_notification():
    print("Creating Notification...")
    
    instance = Notification(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        userId=None,
        
        type=None,
        
        title="example",
        
        message="example",
        
        priority=None,
        
        entityId=None,
        
        entityType=None,
        
        actionUrl=None,
        
        metadata=None,
        
        isRead=True,
        
        readAt=None,
        
        createdAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_notification()
