# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["OrderRetrieveParams"]


class OrderRetrieveParams(TypedDict, total=False):
    customer_partner_id: Annotated[Optional[str], PropertyInfo(alias="customerPartnerId")]
    """Optional customer partner ID for validation"""
