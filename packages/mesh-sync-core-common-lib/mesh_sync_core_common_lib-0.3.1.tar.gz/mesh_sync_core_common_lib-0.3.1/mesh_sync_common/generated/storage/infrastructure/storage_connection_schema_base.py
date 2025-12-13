# AUTO-GENERATED - DO NOT EDIT
# Generated from: StorageConnection infrastructure mapping

from sqlalchemy import Column, Index, DateTime
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base


class StorageConnectionSchemaBase(Base):
    """Represents a connection to a storage provider for scanning and syncing files"""
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    storageProviderConfigId = Column(UUID(as_uuid=True), nullable=False)
    userId = Column(UUID(as_uuid=True), nullable=True)
    libraryId = Column(UUID(as_uuid=True), nullable=True)
    name = Column(String, nullable=False)
    providerType = Column(String, nullable=False)
    rootPath = Column(String, nullable=True)
    isActive = Column(Boolean, nullable=False)
    lastScanStatus = Column(String, nullable=False)
    lastScanError = Column(String, nullable=True)
    encryptedCredentials = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
