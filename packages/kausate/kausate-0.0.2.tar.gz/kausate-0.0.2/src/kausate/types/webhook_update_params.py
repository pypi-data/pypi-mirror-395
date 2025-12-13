# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

from .webhook_status import WebhookStatus

__all__ = ["WebhookUpdateParams"]


class WebhookUpdateParams(TypedDict, total=False):
    api_version: Optional[str]
    """API version for the webhook"""

    custom_headers: Optional[Dict[str, str]]
    """Custom request headers to include in webhook requests"""

    description: Optional[str]
    """Optional description"""

    name: Optional[str]
    """Name of the webhook"""

    partner_customer_id: Optional[str]
    """Optional partner customer ID"""

    status: Optional[WebhookStatus]
    """Status of a webhook configuration."""

    url: Optional[str]
    """URL to receive webhook notifications"""
