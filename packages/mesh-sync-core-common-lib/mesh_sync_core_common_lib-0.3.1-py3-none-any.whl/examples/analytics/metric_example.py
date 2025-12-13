"""
Example usage for Metric
"""
import uuid
from datetime import datetime
from mesh_sync_common.domain.analytics.metric import Metric

def example_metric():
    print("Creating Metric...")
    
    instance = Metric(
        id=UUID('12345678-1234-5678-1234-567812345678'),
        
        userId=None,
        
        type=None,
        
        entityId="example",
        
        entityType="example",
        
        value=None,
        
        metadata=None,
        
        recordedAt=datetime.now(),
        
    )
    
    print(f"Created: {instance}")
    return instance

if __name__ == "__main__":
    example_metric()
