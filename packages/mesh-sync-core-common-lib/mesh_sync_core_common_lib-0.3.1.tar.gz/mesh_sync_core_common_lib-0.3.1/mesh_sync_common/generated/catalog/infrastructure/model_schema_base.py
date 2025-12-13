# AUTO-GENERATED - DO NOT EDIT
# Generated from: Model infrastructure mapping

from sqlalchemy import Column, Index, DateTime
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base


class ModelSchemaBase(Base):
    """Represents a 3D model asset in the system"""
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    fileName = Column(String, nullable=False)
    status = Column(String, nullable=False)
    fileSize = Column(Float, nullable=False)
    # Embedded Value Object: dimensions
    dimension_width = Column(Float, nullable=True)
    dimension_height = Column(Float, nullable=True)
    dimension_depth = Column(Float, nullable=True)
    ownerId = Column(UUID(as_uuid=True), nullable=False)
    libraryId = Column(UUID(as_uuid=True), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
