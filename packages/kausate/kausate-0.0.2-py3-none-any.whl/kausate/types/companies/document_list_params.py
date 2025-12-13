# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["DocumentListParams"]


class DocumentListParams(TypedDict, total=False):
    sync: bool
    """Return result synchronously (default: true)"""

    customer_reference: Annotated[Optional[str], PropertyInfo(alias="customerReference")]

    x_partner_customer_id: Annotated[str, PropertyInfo(alias="X-Partner-Customer-Id")]
    """Optional partner customer ID"""
