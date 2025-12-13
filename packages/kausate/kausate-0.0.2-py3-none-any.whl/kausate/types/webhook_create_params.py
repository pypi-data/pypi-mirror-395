# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

from .webhook_status import WebhookStatus

__all__ = ["WebhookCreateParams"]


class WebhookCreateParams(TypedDict, total=False):
    name: Required[str]
    """Name of the webhook"""

    url: Required[str]
    """URL to receive webhook notifications"""

    api_version: str
    """API version for the webhook"""

    custom_headers: Optional[Dict[str, str]]
    """Custom request headers to include in webhook requests"""

    description: Optional[str]
    """Optional description"""

    partner_customer_id: Optional[str]
    """Optional partner customer ID"""

    status: WebhookStatus
    """Webhook status"""
