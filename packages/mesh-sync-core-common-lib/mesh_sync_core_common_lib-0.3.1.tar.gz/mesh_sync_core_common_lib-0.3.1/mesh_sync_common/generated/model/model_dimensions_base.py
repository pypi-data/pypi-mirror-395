# AUTO-GENERATED - DO NOT EDIT
# Generated from: model/domain/model_dimensions_vo.yaml


from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class ModelDimensionsBase:
    """Physical dimensions of a 3D model (all measurements in millimeters for consistency)"""
    width: float
    height: float
    depth: float
    volumeCubicMm: float = None
    surfaceAreaSqMm: float = None
    originalUnit: str = None

    # Computed properties
    @property
    def boundingBoxVolume(self) -> float:
        return self.width * self.height * self.depth

    @property
    def maxDimension(self) -> float:
        return 


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
        if self.volumeCubicMm < 0:
            raise ValueError('volumeCubicMm must be >= 0')
        if self.surfaceAreaSqMm < 0:
            raise ValueError('surfaceAreaSqMm must be >= 0')
