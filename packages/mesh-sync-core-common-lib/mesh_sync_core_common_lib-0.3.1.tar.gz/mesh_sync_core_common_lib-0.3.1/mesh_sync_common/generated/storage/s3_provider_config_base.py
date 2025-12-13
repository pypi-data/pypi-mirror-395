# AUTO-GENERATED - DO NOT EDIT
# Generated from: storage/domain/s3_provider_config_vo.yaml


from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class S3ProviderConfigBase:
    """S3-compatible storage provider configuration"""
    endpoint: str
    region: str
    bucket: str
    useSSL: bool = None
    pathStyle: bool = None

    def __post_init__(self):
        """Validation"""
        if self.endpoint is None:
            raise ValueError('endpoint is required')
        if self.region is None:
            raise ValueError('region is required')
        if self.bucket is None:
            raise ValueError('bucket is required')
