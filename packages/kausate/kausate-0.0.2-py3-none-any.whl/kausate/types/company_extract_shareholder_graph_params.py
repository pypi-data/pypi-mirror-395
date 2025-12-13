# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["CompanyExtractShareholderGraphParams"]


class CompanyExtractShareholderGraphParams(TypedDict, total=False):
    customer_reference: Annotated[Optional[str], PropertyInfo(alias="customerReference")]

    max_depth: Annotated[int, PropertyInfo(alias="maxDepth")]
    """Maximum depth of ownership levels to extract (1-7)"""

    x_partner_customer_id: Annotated[str, PropertyInfo(alias="X-Partner-Customer-Id")]
    """Optional partner customer ID"""
