# AUTO-GENERATED - DO NOT EDIT
# Generated from: media/domain/watermark_vo.yaml


from mesh_sync_common.generated.media.watermark_position_horizontal_base import WatermarkPositionHorizontal

from mesh_sync_common.generated.media.watermark_position_vertical_base import WatermarkPositionVertical

from mesh_sync_common.generated.media.watermark_content_type_base import WatermarkContentType

from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class WatermarkBase:
    """Configuration for media watermark"""
    enabled: bool = None
    positionHorizontal: WatermarkPositionHorizontal = None
    positionVertical: WatermarkPositionVertical = None
    contentType: WatermarkContentType = None
    imagePath: Optional[str] = None
    text: Optional[str] = None
    fontFamily: Optional[str] = None
    fontSize: Optional[int] = None
    opacity: Optional[float] = None

    def __post_init__(self):
        """Validation"""
        if self.enabled is None:
            raise ValueError('enabled is required')
        if self.positionHorizontal is None:
            raise ValueError('positionHorizontal is required')
        if self.positionVertical is None:
            raise ValueError('positionVertical is required')
        if self.contentType is None:
            raise ValueError('contentType is required')
        if self.opacity < 0:
            raise ValueError('opacity must be >= 0')
        if self.opacity > 1:
            raise ValueError('opacity must be <= 1')
