# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Annotated, TypeAlias, TypedDict

from ..._utils import PropertyInfo
from .uk_advanced_query_param import UkAdvancedQueryParam
from .german_advanced_query_param import GermanAdvancedQueryParam

__all__ = ["SearchRealTimeParams", "AdvancedQuery"]


class SearchRealTimeParams(TypedDict, total=False):
    sync: bool
    """If True, wait for results. If False, return workflow ID immediately"""

    advanced_query: Annotated[Optional[AdvancedQuery], PropertyInfo(alias="advancedQuery")]
    """Jurisdiction-specific advanced search query.

    The structure varies based on the 'jurisdiction' field.
    """

    company_name: Annotated[Optional[str], PropertyInfo(alias="companyName")]
    """Company name to search for.

    Either 'companyName' or 'advancedQuery' must be provided.
    """

    customer_reference: Annotated[Optional[str], PropertyInfo(alias="customerReference")]
    """Optional customer reference for tracking"""

    jurisdiction_code: Annotated[str, PropertyInfo(alias="jurisdictionCode")]
    """
    ISO 3166-1 alpha-2 country code (e.g., 'de' for Germany, 'uk' for United
    Kingdom)
    """

    x_partner_customer_id: Annotated[str, PropertyInfo(alias="X-Partner-Customer-Id")]
    """Optional partner customer ID"""


AdvancedQuery: TypeAlias = Union[GermanAdvancedQueryParam, UkAdvancedQueryParam]
