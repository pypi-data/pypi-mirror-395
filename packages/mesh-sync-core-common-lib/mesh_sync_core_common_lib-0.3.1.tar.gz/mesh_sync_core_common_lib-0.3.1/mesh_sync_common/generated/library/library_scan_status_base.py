# AUTO-GENERATED - DO NOT EDIT
# Generated from: library/domain/library_scan_status_enum.yaml

from enum import Enum


class LibraryScanStatus(Enum):
    """Status of the library scanning process"""
    IDLE = 'idle'
    SCANNING = 'scanning'
    COMPLETED = 'completed'
    FAILED = 'failed'
