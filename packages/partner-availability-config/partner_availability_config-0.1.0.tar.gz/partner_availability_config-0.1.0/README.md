# Partner Availability Configuration

Simple Python package for managing partner availability configurations across tenants.

## Installation

```bash
pip install partner-availability-config
```

## Usage

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from partner_availability import PartnerAvailabilityService, Base

# Setup your database connection
engine = create_engine("postgresql://user:pass@localhost/db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

# Initialize service
service = PartnerAvailabilityService(get_session=SessionLocal)

# Use the 3 core methods
# 1. Get enabled partners
partners = service.get_enabled_partners("tenant1")

# 2. Check if partner is active
is_active = service.is_partner_active("tenant1", "partner_a")

# 3. Update configuration
service.update_partner_config("tenant1", {
    "enabled_partners": ["partner_a", "partner_b"],
    "is_active": True,
    "api_key": "your_api_key"
})
```

## Database Schema

The package creates a `partner_availability_config` table:

- `tenant` (VARCHAR, PRIMARY KEY) - Tenant identifier
- `is_active` (BOOLEAN) - Whether configuration is active
- `api_key` (VARCHAR) - API key for tenant
- `enabled_partners` (JSON) - List of enabled partner identifiers

## Methods

### `get_enabled_partners(tenant: str) -> List[str]`
Returns list of enabled partner identifiers for a tenant.

### `is_partner_active(tenant: str, partner_id: str) -> bool`
Returns True if partner is active for the tenant.

### `update_partner_config(tenant: str, config_data: Dict) -> None`
Updates or creates partner configuration for a tenant.

