# AUTO-GENERATED - DO NOT EDIT
# Generated from: storage/domain/google_drive_provider_config_vo.yaml


from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class GoogleDriveProviderConfigBase:
    """Google Drive storage provider configuration"""
    clientId: str
    folderId: Optional[str] = None
    includeSharedDrives: bool = None
    pageSize: int = None

    def __post_init__(self):
        """Validation"""
        if self.clientId is None:
            raise ValueError('clientId is required')
        if self.pageSize < 1:
            raise ValueError('pageSize must be >= 1')
        if self.pageSize > 1000:
            raise ValueError('pageSize must be <= 1000')
