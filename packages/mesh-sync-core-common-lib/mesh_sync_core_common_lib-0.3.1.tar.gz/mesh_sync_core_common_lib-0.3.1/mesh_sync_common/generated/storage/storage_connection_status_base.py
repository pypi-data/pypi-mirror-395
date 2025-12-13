# AUTO-GENERATED - DO NOT EDIT
# Generated from: storage/domain/storage_connection_status_enum.yaml

from enum import Enum


class StorageConnectionStatus(Enum):
    """Status of a storage connection"""
    CONNECTED = 'connected'
    DISCONNECTED = 'disconnected'
    NEEDS_REAUTH = 'needs_reauth'
    ERROR = 'error'
    UNKNOWN = 'unknown'
    PENDING = 'pending'
