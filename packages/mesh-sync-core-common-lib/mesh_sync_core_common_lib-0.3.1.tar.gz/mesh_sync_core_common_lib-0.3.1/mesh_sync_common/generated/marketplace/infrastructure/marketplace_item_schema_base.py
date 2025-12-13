# AUTO-GENERATED - DO NOT EDIT
# Generated from: MarketplaceItem infrastructure mapping

from sqlalchemy import Column, Index, DateTime
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base


class MarketplaceItemSchemaBase(Base):
    """Represents an item listed on a specific marketplace, linked to an internal Model"""
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    modelId = Column(UUID(as_uuid=True), nullable=False)
    userId = Column(UUID(as_uuid=True), nullable=False)
    marketplace = Column(String, nullable=False)
    marketplaceSpecificId = Column(String, nullable=False)
    externalCategoryId = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(String, nullable=False)
    url = Column(String, nullable=False)
    tags = Column(String, nullable=False)
    stats = Column(String, nullable=False)
    syncError = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
