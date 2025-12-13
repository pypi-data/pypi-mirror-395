# AUTO-GENERATED - DO NOT EDIT
# Generated from: model/domain/model_customizations_vo.yaml


from typing import List

from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class ModelCustomizationsBase:
    """Collection of customization categories for a model"""
    categories: List[CustomizationCategory] = None

    def __post_init__(self):
        """Validation"""
        if self.categories is None:
            raise ValueError('categories is required')
