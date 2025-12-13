# AUTO-GENERATED - DO NOT EDIT
# Generated from: model/domain/model_status_enum.yaml

from enum import Enum


class ModelStatus(Enum):
    """Status of a model throughout its lifecycle from discovery to marketplace listing"""
    DISCOVERED = 'discovered'
    PENDING_RAW_MODEL_PERSISTENCE = 'pending_raw_model_persistence'
    PENDING_ENRICHMENT = 'pending_enrichment'
    PROCESSED = 'processed'
    LISTED = 'listed'
    ERROR = 'error'
    ERROR_UNSUPPORTED_FORMAT = 'error_unsupported_format'
    ERROR_PROCESSING_FAILED = 'error_processing_failed'
    ERROR_TOO_LARGE = 'error_too_large'
    WARNING = 'warning'
    PROCESSING = 'processing'
    ERROR_PROCESSING_ATTEMPT_FAILED = 'error_processing_attempt_failed'
    PROCESSING_LARGE_FILE = 'processing_large_file'
    IGNORED = 'ignored'
    DOWNLOADED = 'downloaded'
    ANALYZED = 'analyzed'
    WAITING_FOR_FOLDER = 'waiting_for_folder'
    METAMODEL_GROUPED = 'metamodel_grouped'
    ENRICHED = 'enriched'
    METADATA_GENERATED = 'metadata_generated'
    NEEDS_REFINEMENT = 'needs_refinement'
    READY = 'ready'
    PENDING_REVIEW = 'pending_review'
    CACHE_CLEANED = 'cache_cleaned'
