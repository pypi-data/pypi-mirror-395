"""
Example usage for Library
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.library.library import Library

def example_library():
    print("Creating Library...")
    
    instance = Library(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        name="example",
        
        path="example",
        
        validationResult=None,
        
        storageProviderConfigId=None,
        
        stats=None,
        
        userId=None,
        
        scanStatus=None,
        
        lastScanTime=None,
        
        createdAt=datetime.now(),
        
        updatedAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_library()
