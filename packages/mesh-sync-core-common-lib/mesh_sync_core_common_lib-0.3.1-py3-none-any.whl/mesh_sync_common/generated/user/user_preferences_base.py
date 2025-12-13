# AUTO-GENERATED - DO NOT EDIT
# Generated from: user/domain/user_preferences_vo.yaml


from uuid import UUID

from mesh_sync_common.generated.user.ui_settings_base import UiSettingsBase

from mesh_sync_common.generated.user.onboarding_status_base import OnboardingStatusBase

from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class UserPreferencesBase:
    """User-specific preferences and settings"""
    defaultMarketplace: str = None
    defaultLibraryId: UUID = None
    uiSettings: Optional[UiSettingsBase] = None
    emailNotifications: bool = None
    onboardingStatus: OnboardingStatusBase = None

    def __post_init__(self):
        """Validation"""
