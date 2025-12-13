# AUTO-GENERATED - DO NOT EDIT
# Generated from: collection/domain/thumbnail_status_enum.yaml

from enum import Enum


class ThumbnailStatus(Enum):
    """Status of the collection thumbnail"""
    NONE = 'none'
    UPLOADED = 'uploaded'
    PENDING = 'pending'
    GENERATING = 'generating'
    GENERATED = 'generated'
    FAILED = 'failed'
    ERROR_UNSUPPORTED_FORMAT = 'error_unsupported_format'
    ERROR_TOO_LARGE_FILE = 'error_too_large_file'
    ERROR_PROCESSING_FAILED = 'error_processing_failed'
    ERROR_MISSING_DATA = 'error_missing_data'
