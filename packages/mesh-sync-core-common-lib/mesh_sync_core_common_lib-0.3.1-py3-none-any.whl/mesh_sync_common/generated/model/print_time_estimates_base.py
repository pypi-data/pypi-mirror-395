# AUTO-GENERATED - DO NOT EDIT
# Generated from: model/domain/print_time_estimates_vo.yaml


from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class PrintTimeEstimatesBase:
    """Print time estimates for different quality levels"""
    draft: Optional[float] = None
    normal: Optional[float] = None
    highQuality: Optional[float] = None

    def __post_init__(self):
        """Validation"""
        if self.draft < 0:
            raise ValueError('draft must be >= 0')
        if self.normal < 0:
            raise ValueError('normal must be >= 0')
        if self.highQuality < 0:
            raise ValueError('highQuality must be >= 0')
