# AUTO-GENERATED - DO NOT EDIT
# Generated from: library/domain/validation_result_vo.yaml


from typing import List

from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class ValidationResultBase:
    """Result of a validation process"""
    errors: List[ValidationError] = None
    warnings: List[ValidationWarning] = None

    def __post_init__(self):
        """Validation"""
        if self.errors is None:
            raise ValueError('errors is required')
        if self.warnings is None:
            raise ValueError('warnings is required')
