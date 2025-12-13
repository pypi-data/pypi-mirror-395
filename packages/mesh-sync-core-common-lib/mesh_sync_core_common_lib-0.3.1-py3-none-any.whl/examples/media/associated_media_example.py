"""
Example usage for AssociatedMedia
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.media.associated_media import AssociatedMedia

def example_associated_media():
    print("Creating AssociatedMedia...")
    
    instance = AssociatedMedia(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        modelId=None,
        
        metamodelId=None,
        
        orderedThumbnailIds=None,
        
        createdAt=datetime.now(),
        
        updatedAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_associated_media()
