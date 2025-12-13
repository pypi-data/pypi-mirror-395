# AUTO-GENERATED - DO NOT EDIT
# Generated from: marketplace/domain/etsy_listing_metadata_vo.yaml


from typing import List

from mesh_sync_common.generated.marketplace.etsy_who_made_base import EtsyWhoMade

from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class EtsyListingMetadataBase:
    """Etsy specific listing metadata"""
    taxonomyId: int
    whoMade: EtsyWhoMade
    whenMade: str
    isDigital: bool
    shippingProfileId: Optional[int] = None
    state: str = None
    quantity: int = None
    materialTags: Optional[List[str]] = None
    processingMin: Optional[int] = None
    processingMax: Optional[int] = None

    def __post_init__(self):
        """Validation"""
        if self.taxonomyId is None:
            raise ValueError('taxonomyId is required')
        if self.whoMade is None:
            raise ValueError('whoMade is required')
        if self.whenMade is None:
            raise ValueError('whenMade is required')
        if self.isDigital is None:
            raise ValueError('isDigital is required')
        if self.state is None:
            raise ValueError('state is required')
        if self.quantity is None:
            raise ValueError('quantity is required')
