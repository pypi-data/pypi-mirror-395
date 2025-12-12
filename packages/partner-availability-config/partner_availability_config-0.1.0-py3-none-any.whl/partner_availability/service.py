"""
Service for partner availability configuration.
"""

from typing import List, Dict, Callable, Optional
from sqlalchemy.orm import Session
from partner_availability.models import PartnerAvailabilityConfig


class PartnerAvailabilityService:
    """Service for managing partner availability configurations."""
    
    def __init__(self, get_session: Callable[[], Session]):
        """
        Initialize service.
        
        Args:
            get_session: Callable that returns a SQLAlchemy Session
        """
        self.get_session = get_session
    
    def get_enabled_partners(self, tenant: str) -> List[str]:
        """
        Get list of enabled partners for a tenant.
        
        Args:
            tenant: Tenant identifier
            
        Returns:
            List of enabled partner identifiers
        """
        session = self.get_session()
        try:
            config = (
                session.query(PartnerAvailabilityConfig)
                .filter(PartnerAvailabilityConfig.tenant == tenant)
                .first()
            )
            if config and config.is_active:
                return config.enabled_partners or []
            return []
        finally:
            session.close()
    
    def is_partner_active(self, tenant: str, partner_id: str) -> bool:
        """
        Check if a specific partner is active for a tenant.
        
        Args:
            tenant: Tenant identifier
            partner_id: Partner identifier to check
            
        Returns:
            True if partner is active, False otherwise
        """
        enabled_partners = self.get_enabled_partners(tenant)
        return partner_id in enabled_partners
    
    def update_partner_config(self, tenant: str, config_data: Dict) -> None:
        """
        Update partner configuration for a tenant.
        
        Args:
            tenant: Tenant identifier
            config_data: Configuration data dictionary with keys:
                - is_active (optional): Boolean
                - api_key (optional): String
                - enabled_partners (optional): List of partner identifiers
        """
        if not tenant:
            raise ValueError("tenant is required")
        
        session = self.get_session()
        try:
            config = (
                session.query(PartnerAvailabilityConfig)
                .filter(PartnerAvailabilityConfig.tenant == tenant)
                .first()
            )
            
            if config:
                if "is_active" in config_data:
                    config.is_active = config_data["is_active"]
                if "api_key" in config_data:
                    config.api_key = config_data["api_key"]
                if "enabled_partners" in config_data:
                    config.enabled_partners = config_data["enabled_partners"]
            else:
                if "api_key" not in config_data:
                    raise ValueError("api_key is required for new configurations")
                
                config = PartnerAvailabilityConfig(
                    tenant=tenant,
                    is_active=config_data.get("is_active", True),
                    api_key=config_data["api_key"],
                    enabled_partners=config_data.get("enabled_partners", []),
                )
                session.add(config)
            
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
