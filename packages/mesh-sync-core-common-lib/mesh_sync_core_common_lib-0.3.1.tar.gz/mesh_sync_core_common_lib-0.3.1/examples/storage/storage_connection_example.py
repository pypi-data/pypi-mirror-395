"""
Example usage for StorageConnection
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.storage.storage_connection import StorageConnection

def example_storage_connection():
    print("Creating StorageConnection...")
    
    instance = StorageConnection(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        storageProviderConfigId=None,
        
        name="example",
        
        providerType=None,
        
        userId=None,
        
        libraryId=None,
        
        rootPath=None,
        
        isActive=True,
        
        lastScanStatus=None,
        
        lastScanError=None,
        
        lastScanAt=None,
        
        encryptedCredentials=None,
        
        createdAt=datetime.now(),
        
        updatedAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_storage_connection()
