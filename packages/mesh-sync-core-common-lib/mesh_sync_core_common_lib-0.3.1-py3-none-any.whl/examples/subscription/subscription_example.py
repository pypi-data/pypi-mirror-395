"""
Example usage for Subscription
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.subscription.subscription import Subscription

def example_subscription():
    print("Creating Subscription...")
    
    instance = Subscription(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        userId=None,
        
        planId=None,
        
        startDate=datetime.now(),
        
        endDate=None,
        
        status=None,
        
        stripeCustomerId=None,
        
        stripeSubscriptionId=None,
        
        currentPeriodEnd=None,
        
        cancelAtPeriodEnd=True,
        
        paymentMethodId=None,
        
        createdAt=datetime.now(),
        
        updatedAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_subscription()
