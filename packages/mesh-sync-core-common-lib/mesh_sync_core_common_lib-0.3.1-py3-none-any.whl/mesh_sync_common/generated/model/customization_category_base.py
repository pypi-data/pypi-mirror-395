# AUTO-GENERATED - DO NOT EDIT
# Generated from: model/domain/customization_category_vo.yaml


from typing import List

from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class CustomizationCategoryBase:
    """A category of customization options"""
    name: str
    options: List[CustomizationOption] = None
    required: bool = None
    allowMultiple: bool = None

    def __post_init__(self):
        """Validation"""
        if self.name is None:
            raise ValueError('name is required')
        if self.options is None:
            raise ValueError('options is required')
        if self.required is None:
            raise ValueError('required is required')
        if self.allowMultiple is None:
            raise ValueError('allowMultiple is required')
