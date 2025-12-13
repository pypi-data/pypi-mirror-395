# AUTO-GENERATED - DO NOT EDIT
# Generated from: marketplace/domain/marketplace_listing_status_enum.yaml

from enum import Enum


class MarketplaceListingStatus(Enum):
    """Status of the marketplace listing"""
    DRAFT = 'draft'
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    SOLD = 'sold'
    EXPIRED = 'expired'
    ARCHIVED = 'archived'
    ERROR = 'error'
    UNKNOWN = 'unknown'
