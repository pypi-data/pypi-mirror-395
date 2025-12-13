# AUTO-GENERATED - DO NOT EDIT
# Generated from: user/domain/ui_settings_vo.yaml


from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class UiSettingsBase:
    """User interface settings and customizations"""
    theme: Optional[str] = None
    language: Optional[str] = None
    compactMode: bool = None
    sidebarCollapsed: bool = None
    itemsPerPage: int = None

    def __post_init__(self):
        """Validation"""
        if self.itemsPerPage < 10:
            raise ValueError('itemsPerPage must be >= 10')
        if self.itemsPerPage > 100:
            raise ValueError('itemsPerPage must be <= 100')
