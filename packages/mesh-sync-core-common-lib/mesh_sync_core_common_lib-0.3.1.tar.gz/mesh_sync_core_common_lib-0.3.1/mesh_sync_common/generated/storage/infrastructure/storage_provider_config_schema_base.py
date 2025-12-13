# AUTO-GENERATED - DO NOT EDIT
# Generated from: StorageProviderConfig infrastructure mapping

from sqlalchemy import Column, Index, DateTime
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base


class StorageProviderConfigSchemaBase(Base):
    """Configuration for a specific instance of a storage provider connection"""
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    userId = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    scanRootPath = Column(String, nullable=False)
    maxScanDepth = Column(String, nullable=False)
    configuration = Column(String, nullable=False)
    encryptedCredentials = Column(String, nullable=False)
    isConnected = Column(Boolean, nullable=False)
    lastConnectionError = Column(String, nullable=True)
    modelIdentificationRules = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
