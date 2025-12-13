"""
Base Aggregate for Subscription
Generated Code - Do not edit.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import uuid


from uuid import UUID

from mesh_sync_common.generated.subscription.plan_tier_base import PlanTier

from datetime import datetime

from mesh_sync_common.generated.subscription.subscription_status_base import SubscriptionStatus


class SubscriptionBase:
    """
    Represents a user subscription to a plan
    """
    
    def __init__(
        self,
        id: UUID,
        
        userId: UUID,
        
        planId: PlanTier,
        
        startDate: datetime,
        
        endDate: Optional[datetime] = None,
        
        status: SubscriptionStatus = None,
        
        stripeCustomerId: Optional[str] = None,
        
        stripeSubscriptionId: Optional[str] = None,
        
        currentPeriodEnd: Optional[datetime] = None,
        
        cancelAtPeriodEnd: bool = None,
        
        paymentMethodId: Optional[str] = None,
        
        createdAt: datetime = None,
        
        updatedAt: datetime = None,
        
    ):
        # Validate all fields
        self._validate(
            id=id,
            
            userId=userId,
            
            planId=planId,
            
            startDate=startDate,
            
            endDate=endDate,
            
            status=status,
            
            stripeCustomerId=stripeCustomerId,
            
            stripeSubscriptionId=stripeSubscriptionId,
            
            currentPeriodEnd=currentPeriodEnd,
            
            cancelAtPeriodEnd=cancelAtPeriodEnd,
            
            paymentMethodId=paymentMethodId,
            
            createdAt=createdAt,
            
            updatedAt=updatedAt,
            
        )
        
        self._id = id
        
        self._userId = userId
        
        self._planId = planId
        
        self._startDate = startDate
        
        self._endDate = endDate
        
        self._status = status
        
        self._stripeCustomerId = stripeCustomerId
        
        self._stripeSubscriptionId = stripeSubscriptionId
        
        self._currentPeriodEnd = currentPeriodEnd
        
        self._cancelAtPeriodEnd = cancelAtPeriodEnd
        
        self._paymentMethodId = paymentMethodId
        
        self._createdAt = createdAt
        
        self._updatedAt = updatedAt
        

    def _validate(self, **kwargs) -> None:
        """Validate all required fields and constraints"""
        errors = []
        
        # Identity validation
        if kwargs.get('id') is None:
            errors.append('id is required')
        
        
        
        # userId: required field
        if kwargs.get('userId') is None:
            errors.append('userId is required')
        
        
        
        
        
        
        # planId: required field
        if kwargs.get('planId') is None:
            errors.append('planId is required')
        
        
        
        
        
        
        # startDate: required field
        if kwargs.get('startDate') is None:
            errors.append('startDate is required')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if errors:
            raise ValueError('; '.join(errors))

    @property
    def id(self) -> UUID:
        return self._id

    
    @property
    def userId(self) -> UUID:
        return self._userId
    
    @userId.setter
    def userId(self, value: UUID):
        self._userId = value
    
    @property
    def planId(self) -> PlanTier:
        return self._planId
    
    @planId.setter
    def planId(self, value: PlanTier):
        self._planId = value
    
    @property
    def startDate(self) -> datetime:
        return self._startDate
    
    @startDate.setter
    def startDate(self, value: datetime):
        self._startDate = value
    
    @property
    def endDate(self) -> Optional[datetime]:
        return self._endDate
    
    @endDate.setter
    def endDate(self, value: Optional[datetime]):
        self._endDate = value
    
    @property
    def status(self) -> SubscriptionStatus:
        return self._status
    
    @status.setter
    def status(self, value: SubscriptionStatus):
        self._status = value
    
    @property
    def stripeCustomerId(self) -> Optional[str]:
        return self._stripeCustomerId
    
    @stripeCustomerId.setter
    def stripeCustomerId(self, value: Optional[str]):
        self._stripeCustomerId = value
    
    @property
    def stripeSubscriptionId(self) -> Optional[str]:
        return self._stripeSubscriptionId
    
    @stripeSubscriptionId.setter
    def stripeSubscriptionId(self, value: Optional[str]):
        self._stripeSubscriptionId = value
    
    @property
    def currentPeriodEnd(self) -> Optional[datetime]:
        return self._currentPeriodEnd
    
    @currentPeriodEnd.setter
    def currentPeriodEnd(self, value: Optional[datetime]):
        self._currentPeriodEnd = value
    
    @property
    def cancelAtPeriodEnd(self) -> bool:
        return self._cancelAtPeriodEnd
    
    @cancelAtPeriodEnd.setter
    def cancelAtPeriodEnd(self, value: bool):
        self._cancelAtPeriodEnd = value
    
    @property
    def paymentMethodId(self) -> Optional[str]:
        return self._paymentMethodId
    
    @paymentMethodId.setter
    def paymentMethodId(self, value: Optional[str]):
        self._paymentMethodId = value
    
    @property
    def createdAt(self) -> datetime:
        return self._createdAt
    
    @createdAt.setter
    def createdAt(self, value: datetime):
        self._createdAt = value
    
    @property
    def updatedAt(self) -> datetime:
        return self._updatedAt
    
    @updatedAt.setter
    def updatedAt(self, value: datetime):
        self._updatedAt = value
    

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SubscriptionBase):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"Subscription(id={self.id})"
