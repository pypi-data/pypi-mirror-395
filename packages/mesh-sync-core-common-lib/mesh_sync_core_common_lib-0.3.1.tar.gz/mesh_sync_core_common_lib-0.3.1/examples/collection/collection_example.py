"""
Example usage for Collection
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.collection.collection import Collection

def example_collection():
    print("Creating Collection...")
    
    instance = Collection(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        userId=None,
        
        name="example",
        
        description=None,
        
        isPublic=True,
        
        thumbnailType=None,
        
        thumbnailProcessedPath=None,
        
        thumbnailStatus=None,
        
        thumbnailSourcePath=None,
        
        thumbnailSourceConnectionId=None,
        
        modelIds=None,
        
        createdAt=datetime.now(),
        
        updatedAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_collection()
