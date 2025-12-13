# AUTO-GENERATED - DO NOT EDIT
# Generated from: analytics/domain/metric_type_enum.yaml

from enum import Enum


class MetricType(Enum):
    """Type of the analytic metric"""
    MODEL_VIEW = 'model_view'
    MODEL_DOWNLOAD = 'model_download'
    MODEL_LIKE = 'model_like'
    MODEL_SHARE = 'model_share'
    LISTING_VIEW = 'listing_view'
    LISTING_FAVORITE = 'listing_favorite'
    LISTING_INQUIRY = 'listing_inquiry'
    SALE = 'sale'
    REVENUE = 'revenue'
    REFUND = 'refund'
