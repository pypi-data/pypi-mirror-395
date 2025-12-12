"""
Database model for partner availability configuration.
"""

from sqlalchemy import Column, String, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PartnerAvailabilityConfig(Base):
    """Database model for partner availability configuration."""
    
    __tablename__ = "partner_availability_config"
    
    tenant = Column(String(255), primary_key=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    api_key = Column(String(255), nullable=False)
    enabled_partners = Column(JSON, nullable=False, default=list)
