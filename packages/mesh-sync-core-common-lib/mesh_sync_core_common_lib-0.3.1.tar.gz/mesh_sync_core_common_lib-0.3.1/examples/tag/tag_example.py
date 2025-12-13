"""
Example usage for Tag
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.tag.tag import Tag

def example_tag():
    print("Creating Tag...")
    
    instance = Tag(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        name="example",
        
        userId=None,
        
        createdAt=datetime.now(),
        
        updatedAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_tag()
