# AUTO-GENERATED - DO NOT EDIT
# Generated from: library/domain/validation_warning_vo.yaml


from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class ValidationWarningBase:
    """Represents a specific validation warning"""
    code: str
    message: str
    path: str = None
    details: Any = None

    def __post_init__(self):
        """Validation"""
        if self.code is None:
            raise ValueError('code is required')
        if self.message is None:
            raise ValueError('message is required')
