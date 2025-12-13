"""
Example usage for Metamodel
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.metamodel.metamodel import Metamodel

def example_metamodel():
    print("Creating Metamodel...")
    
    instance = Metamodel(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        name="example",
        
        ownerId=None,
        
        libraryId=None,
        
        status=None,
        
        storageItemIds=None,
        
        confidenceScore=None,
        
        sellabilityScore=None,
        
        associatedMediaId=None,
        
        internalId=None,
        
        parentMetamodelId=None,
        
        childMetamodelIds=None,
        
        createdAt=datetime.now(),
        
        updatedAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_metamodel()
