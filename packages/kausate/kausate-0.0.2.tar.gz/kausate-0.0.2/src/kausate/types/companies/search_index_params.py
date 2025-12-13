# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Annotated, TypeAlias, TypedDict

from ..._utils import PropertyInfo
from .uk_advanced_query_param import UkAdvancedQueryParam
from .german_advanced_query_param import GermanAdvancedQueryParam

__all__ = ["SearchIndexParams", "AdvancedQuery"]


class SearchIndexParams(TypedDict, total=False):
    advanced_query: Annotated[Optional[AdvancedQuery], PropertyInfo(alias="advancedQuery")]
    """Jurisdiction-specific advanced search query.

    The structure varies based on the 'jurisdiction' field.
    """

    include_alternative_names: Annotated[bool, PropertyInfo(alias="includeAlternativeNames")]
    """If true, searches alternative company names (more expensive).

    Default: false for optimal performance.
    """

    include_similar_names: Annotated[bool, PropertyInfo(alias="includeSimilarNames")]
    """
    If true, falls back to trigram similarity search when no exact matches found
    (more expensive). Default: false for optimal performance.
    """

    jurisdiction_code: Annotated[str, PropertyInfo(alias="jurisdictionCode")]
    """
    ISO 3166-1 alpha-2 country code (e.g., 'de' for Germany, 'uk' for United
    Kingdom)
    """

    limit: Optional[int]

    name: Optional[str]
    """Company name to search for. Either 'name' or 'advancedQuery' must be provided."""

    page: Optional[int]
    """Page number (0-based)"""

    x_partner_customer_id: Annotated[str, PropertyInfo(alias="X-Partner-Customer-Id")]
    """Optional partner customer ID"""


AdvancedQuery: TypeAlias = Union[GermanAdvancedQueryParam, UkAdvancedQueryParam]
