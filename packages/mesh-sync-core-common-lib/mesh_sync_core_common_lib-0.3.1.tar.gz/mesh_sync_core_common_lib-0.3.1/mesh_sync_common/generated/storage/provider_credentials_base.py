# AUTO-GENERATED - DO NOT EDIT
# Generated from: storage/domain/provider_credentials_vo.yaml


from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class ProviderCredentialsBase:
    """Encrypted credentials for storage provider access"""
    password: Optional[str] = None
    privateKey: Optional[str] = None
    accessKeyId: Optional[str] = None
    secretAccessKey: Optional[str] = None
    refreshToken: Optional[str] = None
    accessToken: Optional[str] = None

    def __post_init__(self):
        """Validation"""
