# AUTO-GENERATED - DO NOT EDIT
# Generated from: storage/domain/sftp_provider_config_vo.yaml


from mesh_sync_common.generated.storage.sftp_auth_method_base import SftpAuthMethod

from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class SftpProviderConfigBase:
    """SFTP-specific storage provider configuration"""
    host: str
    username: str
    authMethod: SftpAuthMethod
    port: int = None
    passiveMode: bool = None
    timeout: int = None

    def __post_init__(self):
        """Validation"""
        if self.host is None:
            raise ValueError('host is required')
        if self.username is None:
            raise ValueError('username is required')
        if self.authMethod is None:
            raise ValueError('authMethod is required')
        if self.port is None:
            raise ValueError('port is required')
        if self.port < 1:
            raise ValueError('port must be >= 1')
        if self.port > 65535:
            raise ValueError('port must be <= 65535')
        if self.timeout < 1000:
            raise ValueError('timeout must be >= 1000')
