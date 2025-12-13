# AUTO-GENERATED - DO NOT EDIT
# Generated from: marketplace/domain/marketplace_item_status_enum.yaml

from enum import Enum


class MarketplaceItemStatus(Enum):
    """Status of a marketplace listing item"""
    DRAFT = 'draft'
    PENDING_SYNC = 'pending_sync'
    SYNCING = 'syncing'
    PUBLISHED = 'published'
    ACTIVE = 'active'
    ERROR = 'error'
    FAILED = 'failed'
    ARCHIVED = 'archived'
