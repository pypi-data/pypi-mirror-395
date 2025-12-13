# AUTO-GENERATED - DO NOT EDIT
# Generated from: Tag infrastructure mapping

from sqlalchemy import Column, Index, DateTime
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base


class TagSchemaBase(Base):
    """Represents a user-defined tag for organizing models"""
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    userId = Column(UUID(as_uuid=True), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
