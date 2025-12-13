"""
Example usage for MarketplaceItem
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.marketplace.marketplace_item import MarketplaceItem

def example_marketplace_item():
    print("Creating MarketplaceItem...")
    
    instance = MarketplaceItem(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        modelId=None,
        
        userId=None,
        
        marketplace="example",
        
        title="example",
        
        description="example",
        
        price=None,
        
        currency="example",
        
        marketplaceSpecificId="example",
        
        externalCategoryId="example",
        
        status=None,
        
        url="example",
        
        tags=None,
        
        stats=None,
        
        lastSyncTime=datetime.now(),
        
        syncError="example",
        
        createdAt=datetime.now(),
        
        updatedAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_marketplace_item()
