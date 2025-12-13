"""
Example usage for MarketplaceListing
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.marketplace.marketplace_listing import MarketplaceListing

def example_marketplace_listing():
    print("Creating MarketplaceListing...")
    
    instance = MarketplaceListing(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        modelId=None,
        
        marketplaceId="example",
        
        marketplaceSpecificId="example",
        
        title="example",
        
        description="example",
        
        price=None,
        
        currency="example",
        
        quantity=1,
        
        stats=None,
        
        url=None,
        
        tags=None,
        
        taxonomyId=None,
        
        isDigital=True,
        
        status=None,
        
        etsyMetadata=None,
        
        lastSyncAt=None,
        
        createdAt=datetime.now(),
        
        updatedAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_marketplace_listing()
