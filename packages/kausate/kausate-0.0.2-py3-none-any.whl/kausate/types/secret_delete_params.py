# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["SecretDeleteParams"]


class SecretDeleteParams(TypedDict, total=False):
    partner_customer_id: Annotated[Optional[str], PropertyInfo(alias="partnerCustomerId")]
    """Partner customer ID"""
