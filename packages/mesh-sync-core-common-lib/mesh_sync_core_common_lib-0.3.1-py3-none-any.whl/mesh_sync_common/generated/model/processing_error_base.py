# AUTO-GENERATED - DO NOT EDIT
# Generated from: model/domain/processing_error_vo.yaml


from mesh_sync_common.generated.model.error_code_base import ErrorCode

from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class ProcessingErrorBase:
    """Represents an error that occurred during model processing"""
    code: ErrorCode
    message: str

    # Computed properties
    @property
    def hasError(self) -> bool:
        return self.code != ErrorCode.NONE


    def __post_init__(self):
        """Validation"""
        if self.code is None:
            raise ValueError('code is required')
        if self.message is None:
            raise ValueError('message is required')
