# AUTO-GENERATED - DO NOT EDIT
# Generated from: model/domain/print_estimates_vo.yaml


from mesh_sync_common.generated.model.print_time_estimates_base import PrintTimeEstimatesBase

from mesh_sync_common.generated.model.material_estimates_base import MaterialEstimatesBase

from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class PrintEstimatesBase:
    """3D print estimates providing time and material usage predictions"""
    requiresSupports: bool
    estimatedPrintTimeMinutes: float = None
    estimatedMaterialGrams: float = None
    printTimeEstimates: Optional[PrintTimeEstimatesBase] = None
    materialEstimates: Optional[MaterialEstimatesBase] = None

    # Computed properties
    @property
    def estimatedPrintTimeHours(self) -> float:
        return self.estimatedPrintTimeMinutes / 60

    @property
    def formattedPrintTime(self) -> str:
        return 


    def __post_init__(self):
        """Validation"""
        if self.requiresSupports is None:
            raise ValueError('requiresSupports is required')
        if self.estimatedPrintTimeMinutes < 0:
            raise ValueError('estimatedPrintTimeMinutes must be >= 0')
        if self.estimatedMaterialGrams < 0:
            raise ValueError('estimatedMaterialGrams must be >= 0')
