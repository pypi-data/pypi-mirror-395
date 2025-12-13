# AUTO-GENERATED - DO NOT EDIT
# Generated from: model/domain/customization_option_vo.yaml


from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class CustomizationOptionBase:
    """A single customization option"""
    name: str
    priceOffset: float = None
    offsetType: str = None
    description: Optional[str] = None
    sku: Optional[str] = None

    def __post_init__(self):
        """Validation"""
        if self.name is None:
            raise ValueError('name is required')
        if self.priceOffset is None:
            raise ValueError('priceOffset is required')
        if self.offsetType is None:
            raise ValueError('offsetType is required')
