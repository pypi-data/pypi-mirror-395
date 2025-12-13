"""
Example usage for User
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.user.user import User

def example_user():
    print("Creating User...")
    
    instance = User(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        email="example",
        
        name="example",
        
        preferences=None,
        
        role=None,
        
        subscriptionId="example",
        
        lastLogin=datetime.now(),
        
        createdAt=datetime.now(),
        
        updatedAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_user()
