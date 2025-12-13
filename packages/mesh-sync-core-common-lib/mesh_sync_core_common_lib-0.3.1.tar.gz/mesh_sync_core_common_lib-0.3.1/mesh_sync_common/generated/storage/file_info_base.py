# AUTO-GENERATED - DO NOT EDIT
# Generated from: storage/domain/file_info_vo.yaml


from datetime import datetime

from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class FileInfoBase:
    """Information about a file or directory in storage"""
    name: str
    path: str
    size: int
    lastModified: datetime
    isDirectory: bool

    def __post_init__(self):
        """Validation"""
        if self.name is None:
            raise ValueError('name is required')
        if self.path is None:
            raise ValueError('path is required')
        if self.size is None:
            raise ValueError('size is required')
        if self.size < 0:
            raise ValueError('size must be >= 0')
        if self.lastModified is None:
            raise ValueError('lastModified is required')
        if self.isDirectory is None:
            raise ValueError('isDirectory is required')
