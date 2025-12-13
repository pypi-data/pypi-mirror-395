# AUTO-GENERATED - DO NOT EDIT
# Generated from: catalog/domain/model_status_enum.yaml

from enum import Enum


class ModelStatus(Enum):
    """Possible states of a model in the system"""
    DISCOVERED = 'discovered'
    PENDING_RAW_MODEL_PERSISTENCE = 'pending_raw_model_persistence'
    PENDING_ENRICHMENT = 'pending_enrichment'
    PROCESSED = 'processed'
    LISTED = 'listed'
    ERROR = 'error'

DEFAULT_MODEL_STATUS = ModelStatus.DISCOVERED
