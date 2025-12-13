# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["SecretListParams"]


class SecretListParams(TypedDict, total=False):
    datasource_slug: Annotated[Optional[str], PropertyInfo(alias="datasourceSlug")]
    """Filter by datasource slug"""

    partner_customer_id: Annotated[Optional[str], PropertyInfo(alias="partnerCustomerId")]
    """Partner customer ID"""
