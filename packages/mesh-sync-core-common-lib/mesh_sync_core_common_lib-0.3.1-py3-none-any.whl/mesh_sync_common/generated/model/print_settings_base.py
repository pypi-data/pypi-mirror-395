# AUTO-GENERATED - DO NOT EDIT
# Generated from: model/domain/print_settings_vo.yaml


from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class PrintSettingsBase:
    """Recommended or used print settings for 3D printing a model"""
    layerHeight: float = None
    infillPercentage: float = None
    supportsEnabled: bool = None
    raftEnabled: bool = None
    nozzleTemperature: float = None
    bedTemperature: float = None
    printSpeed: float = None
    material: str = None
    notes: str = None

    def __post_init__(self):
        """Validation"""
        if self.layerHeight < 0:
            raise ValueError('layerHeight must be >= 0')
        if self.infillPercentage < 0:
            raise ValueError('infillPercentage must be >= 0')
        if self.infillPercentage > 100:
            raise ValueError('infillPercentage must be <= 100')
        if self.nozzleTemperature < 0:
            raise ValueError('nozzleTemperature must be >= 0')
        if self.bedTemperature < 0:
            raise ValueError('bedTemperature must be >= 0')
        if self.printSpeed < 0:
            raise ValueError('printSpeed must be >= 0')
