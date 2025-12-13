# AUTO-GENERATED - DO NOT EDIT
# Generated from: metamodel/domain/metamodel_rating_vo_vo.yaml


from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class MetamodelRatingVOBase:
    """Value object representing a rating"""
    value: int
    comment: Optional[str] = None

    def __post_init__(self):
        """Validation"""
        if self.value is None:
            raise ValueError('value is required')
        if self.value < 1:
            raise ValueError('value must be >= 1')
        if self.value > 5:
            raise ValueError('value must be <= 5')
