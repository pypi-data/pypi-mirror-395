"""
Example usage for MetamodelRating
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.metamodel.metamodel_rating import MetamodelRating

def example_metamodel_rating():
    print("Creating MetamodelRating...")
    
    instance = MetamodelRating(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        userId=None,
        
        metamodelId=None,
        
        rating=None,
        
        createdAt=datetime.now(),
        
        updatedAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_metamodel_rating()
