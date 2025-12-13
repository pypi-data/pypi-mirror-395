# AUTO-GENERATED - DO NOT EDIT
# Generated from: storage/domain/model_identification_rules_vo.yaml


from typing import List

from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass(frozen=True)
class ModelIdentificationRulesBase:
    """Rules for identifying models during storage scanning operations"""
    significantMediaExtensions: List[str] = None
    condition1MinModelFiles: int = None
    condition1MinSignificantMediaFiles: int = None
    condition2ExactModelFiles: int = None
    condition2ExactSignificantMediaFiles: int = None
    condition2ExactRelevantUnprocessedSubDirs: int = None
    condition2ExactInitialSubDirs: int = None
    disableCondition2ForScanRoot: bool = None
    useParentDirAsSingleModelName: bool = None
    collectionPackIndicatorKeywords: List[str] = None
    cleanFolderNameRegexPattern: Optional[str] = None
    associatedMediaSuffixPatternRegex: Optional[str] = None
    allowExactMediaNameMatch: bool = None
    generalAssociationKeywords: List[str] = None

    def __post_init__(self):
        """Validation"""
        if self.significantMediaExtensions is None:
            raise ValueError('significantMediaExtensions is required')
        if self.condition1MinModelFiles is None:
            raise ValueError('condition1MinModelFiles is required')
        if self.condition1MinModelFiles < 0:
            raise ValueError('condition1MinModelFiles must be >= 0')
        if self.condition1MinSignificantMediaFiles is None:
            raise ValueError('condition1MinSignificantMediaFiles is required')
        if self.condition1MinSignificantMediaFiles < 0:
            raise ValueError('condition1MinSignificantMediaFiles must be >= 0')
        if self.condition2ExactModelFiles is None:
            raise ValueError('condition2ExactModelFiles is required')
        if self.condition2ExactModelFiles < 0:
            raise ValueError('condition2ExactModelFiles must be >= 0')
        if self.condition2ExactSignificantMediaFiles is None:
            raise ValueError('condition2ExactSignificantMediaFiles is required')
        if self.condition2ExactSignificantMediaFiles < 0:
            raise ValueError('condition2ExactSignificantMediaFiles must be >= 0')
        if self.condition2ExactRelevantUnprocessedSubDirs is None:
            raise ValueError('condition2ExactRelevantUnprocessedSubDirs is required')
        if self.condition2ExactRelevantUnprocessedSubDirs < 0:
            raise ValueError('condition2ExactRelevantUnprocessedSubDirs must be >= 0')
        if self.condition2ExactInitialSubDirs is None:
            raise ValueError('condition2ExactInitialSubDirs is required')
        if self.condition2ExactInitialSubDirs < 0:
            raise ValueError('condition2ExactInitialSubDirs must be >= 0')
        if self.disableCondition2ForScanRoot is None:
            raise ValueError('disableCondition2ForScanRoot is required')
        if self.useParentDirAsSingleModelName is None:
            raise ValueError('useParentDirAsSingleModelName is required')
        if self.collectionPackIndicatorKeywords is None:
            raise ValueError('collectionPackIndicatorKeywords is required')
        if self.allowExactMediaNameMatch is None:
            raise ValueError('allowExactMediaNameMatch is required')
        if self.generalAssociationKeywords is None:
            raise ValueError('generalAssociationKeywords is required')
