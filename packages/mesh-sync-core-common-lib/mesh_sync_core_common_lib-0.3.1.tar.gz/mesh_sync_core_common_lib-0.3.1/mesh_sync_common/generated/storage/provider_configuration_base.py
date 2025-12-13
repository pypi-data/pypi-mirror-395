# AUTO-GENERATED - DO NOT EDIT
# Generated from: storage/domain/provider_configuration_vo.yaml


from mesh_sync_common.generated.storage.sftp_provider_config_base import SftpProviderConfigBase

from mesh_sync_common.generated.storage.s3_provider_config_base import S3ProviderConfigBase

from mesh_sync_common.generated.storage.google_drive_provider_config_base import GoogleDriveProviderConfigBase

from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class ProviderConfigurationBase:
    """Union type for provider-specific configurations"""
    sftpConfig: Optional[SftpProviderConfigBase] = None
    s3Config: Optional[S3ProviderConfigBase] = None
    googleDriveConfig: Optional[GoogleDriveProviderConfigBase] = None

    def __post_init__(self):
        """Validation"""
