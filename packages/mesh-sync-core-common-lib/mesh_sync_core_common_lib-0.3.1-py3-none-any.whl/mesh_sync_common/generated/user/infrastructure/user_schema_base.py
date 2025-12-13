# AUTO-GENERATED - DO NOT EDIT
# Generated from: User infrastructure mapping

from sqlalchemy import Column, Index, DateTime
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base


class UserSchemaBase(Base):
    """Represents a user account in the system"""
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    preferences = Column(String, nullable=False)
    subscriptionId = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
