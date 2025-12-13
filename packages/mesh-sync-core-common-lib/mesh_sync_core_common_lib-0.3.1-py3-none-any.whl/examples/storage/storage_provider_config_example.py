"""
Example usage for StorageProviderConfig
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.storage.storage_provider_config import StorageProviderConfig

def example_storage_provider_config():
    print("Creating StorageProviderConfig...")
    
    instance = StorageProviderConfig(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        userId=None,
        
        name="example",
        
        type=None,
        
        scanRootPath="example",
        
        configuration=None,
        
        encryptedCredentials=None,
        
        maxScanDepth=1,
        
        isConnected=True,
        
        lastConnectionAttempt=None,
        
        lastConnectionError=None,
        
        lastScanAt=None,
        
        modelIdentificationRules=None,
        
        createdAt=datetime.now(),
        
        updatedAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_storage_provider_config()
