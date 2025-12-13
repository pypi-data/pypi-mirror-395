# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from .._models import BaseModel
from .webhook_status import WebhookStatus

__all__ = ["WebhookResponse"]


class WebhookResponse(BaseModel):
    id: str
    """Webhook ID"""

    api_version: str
    """API version for the webhook"""

    created_at: datetime
    """Creation timestamp"""

    name: str
    """Name of the webhook"""

    org_id: str
    """Organization ID"""

    status: WebhookStatus
    """Webhook status"""

    updated_at: datetime
    """Last update timestamp"""

    url: str
    """URL to receive webhook notifications"""

    custom_headers: Optional[Dict[str, str]] = None
    """Custom request headers (including Authorization) to include in webhook requests"""

    description: Optional[str] = None
    """Optional description"""

    partner_customer_id: Optional[str] = None
    """Optional partner customer ID"""
