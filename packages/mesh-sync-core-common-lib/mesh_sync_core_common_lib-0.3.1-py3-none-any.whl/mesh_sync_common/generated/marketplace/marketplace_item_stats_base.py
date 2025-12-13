# AUTO-GENERATED - DO NOT EDIT
# Generated from: marketplace/domain/marketplace_item_stats_vo.yaml


from datetime import datetime

from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class MarketplaceItemStatsBase:
    """Statistics for a marketplace listing item"""
    views: int = None
    favorites: int = None
    sales: int = None
    revenue: float = None
    lastRefreshedAt: Optional[datetime] = None

    def __post_init__(self):
        """Validation"""
        if self.views is None:
            raise ValueError('views is required')
        if self.views < 0:
            raise ValueError('views must be >= 0')
        if self.favorites is None:
            raise ValueError('favorites is required')
        if self.favorites < 0:
            raise ValueError('favorites must be >= 0')
        if self.sales is None:
            raise ValueError('sales is required')
        if self.sales < 0:
            raise ValueError('sales must be >= 0')
        if self.revenue is None:
            raise ValueError('revenue is required')
        if self.revenue < 0:
            raise ValueError('revenue must be >= 0')
