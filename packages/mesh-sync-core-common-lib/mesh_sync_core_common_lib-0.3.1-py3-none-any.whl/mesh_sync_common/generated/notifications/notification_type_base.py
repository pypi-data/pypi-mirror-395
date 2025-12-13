# AUTO-GENERATED - DO NOT EDIT
# Generated from: notifications/domain/notification_type_enum.yaml

from enum import Enum


class NotificationType(Enum):
    """Type of the notification"""
    MODEL_DISCOVERED = 'model_discovered'
    MODEL_PROCESSED = 'model_processed'
    MODEL_FAILED = 'model_failed'
    THUMBNAIL_GENERATED = 'thumbnail_generated'
    METADATA_ENHANCED = 'metadata_enhanced'
    LISTING_PUBLISHED = 'listing_published'
    LISTING_UPDATED = 'listing_updated'
    MARKETPLACE_SYNCED = 'marketplace_synced'
    MARKETPLACE_ERROR = 'marketplace_error'
    SALE_COMPLETED = 'sale_completed'
    REFUND_PROCESSED = 'refund_processed'
    PAYOUT_RECEIVED = 'payout_received'
