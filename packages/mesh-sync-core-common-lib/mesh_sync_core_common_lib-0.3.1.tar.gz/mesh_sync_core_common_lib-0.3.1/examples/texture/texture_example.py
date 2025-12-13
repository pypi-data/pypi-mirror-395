"""
Example usage for Texture
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.texture.texture import Texture

def example_texture():
    print("Creating Texture...")
    
    instance = Texture(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        userId=None,
        
        name="example",
        
        type=None,
        
        colorValue=None,
        
        storageItemId=None,
        
        description=None,
        
        isPublic=True,
        
        createdAt=datetime.now(),
        
        updatedAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_texture()
