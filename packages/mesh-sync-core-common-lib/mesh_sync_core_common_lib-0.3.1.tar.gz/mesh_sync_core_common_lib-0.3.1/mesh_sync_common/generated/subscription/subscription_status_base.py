# AUTO-GENERATED - DO NOT EDIT
# Generated from: subscription/domain/subscription_status_enum.yaml

from enum import Enum


class SubscriptionStatus(Enum):
    """Status of the subscription"""
    ACTIVE = 'ACTIVE'
    TRIALING = 'TRIALING'
    PAST_DUE = 'PAST_DUE'
    CANCELED = 'CANCELED'
    ENDED = 'ENDED'
