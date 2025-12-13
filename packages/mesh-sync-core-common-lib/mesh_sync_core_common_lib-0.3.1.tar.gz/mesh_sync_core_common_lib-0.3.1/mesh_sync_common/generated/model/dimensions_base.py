# AUTO-GENERATED - DO NOT EDIT
# Generated from: model/domain/dimensions_vo.yaml


from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class DimensionsBase:
    """Physical dimensions of a 3D model in millimeters"""
    width: float
    height: float
    depth: float

    # Computed properties
    @property
    def volume(self) -> float:
        return self.width * self.height * self.depth


    def __post_init__(self):
        """Validation"""
        if self.width is None:
            raise ValueError('width is required')
        if self.width < 0:
            raise ValueError('width must be >= 0')
        if self.height is None:
            raise ValueError('height is required')
        if self.height < 0:
            raise ValueError('height must be >= 0')
        if self.depth is None:
            raise ValueError('depth is required')
        if self.depth < 0:
            raise ValueError('depth must be >= 0')
