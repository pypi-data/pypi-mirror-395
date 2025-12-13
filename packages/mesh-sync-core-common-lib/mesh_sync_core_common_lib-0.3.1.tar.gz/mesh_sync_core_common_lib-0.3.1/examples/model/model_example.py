"""
Example usage for Model
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.model.model import Model

def example_model():
    print("Creating Model...")
    
    instance = Model(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        name="example",
        
        fileName="example",
        
        fileSize=1,
        
        lastProcessingError=None,
        
        ownerId=None,
        
        libraryId=None,
        
        storageItemId=None,
        
        associatedMediaId=None,
        
        description="example",
        
        generatedDescription="example",
        
        status=None,
        
        fileType="example",
        
        dimensions=None,
        
        printSettings=None,
        
        processing_attempts=1,
        
        tagIds=None,
        
        collectionIds=None,
        
        marketplaceListingIds=None,
        
        parentId=None,
        
        level=1,
        
        geometry=None,
        
        physicalDimensions=None,
        
        quality=None,
        
        printEstimates=None,
        
        customizations=None,
        
        basePrice=None,
        
        baseCurrency="example",
        
        createdAt=datetime.now(),
        
        updatedAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_model()
