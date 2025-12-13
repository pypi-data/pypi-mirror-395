"""
Example usage for ThumbnailMedia
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.media.thumbnail_media import ThumbnailMedia

def example_thumbnail_media():
    print("Creating ThumbnailMedia...")
    
    instance = ThumbnailMedia(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        mediaType=None,
        
        storagePath="example",
        
        originalFileName="example",
        
        mimeType="example",
        
        fileSize=1,
        
        watermark=None,
        
        width=None,
        
        height=None,
        
        duration=None,
        
        createdAt=datetime.now(),
        
        updatedAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_thumbnail_media()
