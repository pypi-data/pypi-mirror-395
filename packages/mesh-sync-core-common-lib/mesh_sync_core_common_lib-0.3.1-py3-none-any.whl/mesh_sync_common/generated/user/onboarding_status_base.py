# AUTO-GENERATED - DO NOT EDIT
# Generated from: user/domain/onboarding_status_vo.yaml


from typing import List

from mesh_sync_common.generated.user.onboarding_state_base import OnboardingState

from datetime import datetime

from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class OnboardingStatusBase:
    """Tracks user's progress through the onboarding process"""
    status: OnboardingState
    currentStep: int = None
    completedSteps: List[str] = None
    startedAt: datetime = None
    completedAt: datetime = None
    skippedAt: datetime = None
    lastUpdatedAt: datetime = None

    # Computed properties
    @property
    def isComplete(self) -> bool:
        return 

    @property
    def progress(self) -> float:
        return 


    def __post_init__(self):
        """Validation"""
        if self.status is None:
            raise ValueError('status is required')
        if self.currentStep < 0:
            raise ValueError('currentStep must be >= 0')
        if self.completedSteps is None:
            raise ValueError('completedSteps is required')
        if self.lastUpdatedAt is None:
            raise ValueError('lastUpdatedAt is required')
