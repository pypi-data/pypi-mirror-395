# AUTO-GENERATED - DO NOT EDIT
# Generated from: library/domain/library_stats_vo.yaml


from datetime import datetime

from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class LibraryStatsBase:
    """Statistics about a Library"""
    totalModels: int = None
    totalFileSize: int = None
    fileTypes: Any = None
    updateTime: datetime = None

    def __post_init__(self):
        """Validation"""
        if self.totalModels is None:
            raise ValueError('totalModels is required')
        if self.totalModels < 0:
            raise ValueError('totalModels must be >= 0')
        if self.totalFileSize is None:
            raise ValueError('totalFileSize is required')
        if self.totalFileSize < 0:
            raise ValueError('totalFileSize must be >= 0')
        if self.fileTypes is None:
            raise ValueError('fileTypes is required')
        if self.updateTime is None:
            raise ValueError('updateTime is required')
