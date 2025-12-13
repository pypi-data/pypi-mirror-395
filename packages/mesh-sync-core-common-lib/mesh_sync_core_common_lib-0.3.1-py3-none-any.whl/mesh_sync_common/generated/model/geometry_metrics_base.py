# AUTO-GENERATED - DO NOT EDIT
# Generated from: model/domain/geometry_metrics_vo.yaml


from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class GeometryMetricsBase:
    """3D model geometry metrics representing mesh complexity and structure"""
    vertices: int
    faces: int
    edges: int

    # Computed properties
    @property
    def detailLevel(self) -> str:
        return 

    @property
    def complexity(self) -> float:
        return self.faces / 1000000


    def __post_init__(self):
        """Validation"""
        if self.vertices is None:
            raise ValueError('vertices is required')
        if self.vertices < 0:
            raise ValueError('vertices must be >= 0')
        if self.faces is None:
            raise ValueError('faces is required')
        if self.faces < 0:
            raise ValueError('faces must be >= 0')
        if self.edges is None:
            raise ValueError('edges is required')
        if self.edges < 0:
            raise ValueError('edges must be >= 0')
