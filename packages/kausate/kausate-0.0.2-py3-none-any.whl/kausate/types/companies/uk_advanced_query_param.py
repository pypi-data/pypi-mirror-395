# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["UkAdvancedQueryParam"]


class UkAdvancedQueryParam(TypedDict, total=False):
    company_number: Required[Annotated[str, PropertyInfo(alias="companyNumber")]]
    """Companies House company number (e.g., '09410276')"""

    jurisdiction: Literal["uk"]
    """
    Jurisdiction discriminator (automatically inferred from jurisdictionCode at API
    level)
    """
