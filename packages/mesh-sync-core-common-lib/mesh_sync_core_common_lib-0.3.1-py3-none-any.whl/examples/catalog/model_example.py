"""
Example usage for Model
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.catalog.model import Model

def example_model():
    print("Creating Model...")
    
    instance = Model(
        ModelId=UUID('12345678-1234-5678-1234-567812345678'),
        
        name="example",
        
        fileName="example",
        
        fileSize=None,
        
        ownerId=None,
        
        libraryId=None,
        
        createdAt=datetime.now(),
        
        updatedAt=datetime.now(),
        
        status=None,
        
        dimensions=None,
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_model()
