# AUTO-GENERATED - DO NOT EDIT
# Generated from: model/domain/material_estimates_vo.yaml


from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class MaterialEstimatesBase:
    """Material usage estimates for different infill percentages"""
    infill10: Optional[float] = None
    infill20: Optional[float] = None
    infill50: Optional[float] = None
    infill100: Optional[float] = None

    def __post_init__(self):
        """Validation"""
        if self.infill10 < 0:
            raise ValueError('infill10 must be >= 0')
        if self.infill20 < 0:
            raise ValueError('infill20 must be >= 0')
        if self.infill50 < 0:
            raise ValueError('infill50 must be >= 0')
        if self.infill100 < 0:
            raise ValueError('infill100 must be >= 0')
