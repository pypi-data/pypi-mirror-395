# AUTO-GENERATED - DO NOT EDIT
# Generated from: model/domain/quality_metrics_vo.yaml


from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class QualityMetricsBase:
    """3D model quality metrics representing mesh quality and printability assessment"""
    manifold: bool
    nonManifoldEdges: int = None
    holes: int = None
    flippedNormals: int = None
    selfIntersections: int = None
    qualityScore: float = None
    printabilityScore: float = None

    # Computed properties
    @property
    def isPrintReady(self) -> bool:
        return 

    @property
    def issueCount(self) -> int:
        return 

    @property
    def qualityLevel(self) -> str:
        return 


    def __post_init__(self):
        """Validation"""
        if self.manifold is None:
            raise ValueError('manifold is required')
        if self.nonManifoldEdges < 0:
            raise ValueError('nonManifoldEdges must be >= 0')
        if self.holes < 0:
            raise ValueError('holes must be >= 0')
        if self.flippedNormals < 0:
            raise ValueError('flippedNormals must be >= 0')
        if self.selfIntersections < 0:
            raise ValueError('selfIntersections must be >= 0')
        if self.qualityScore < 0:
            raise ValueError('qualityScore must be >= 0')
        if self.qualityScore > 100:
            raise ValueError('qualityScore must be <= 100')
        if self.printabilityScore < 0:
            raise ValueError('printabilityScore must be >= 0')
        if self.printabilityScore > 100:
            raise ValueError('printabilityScore must be <= 100')
