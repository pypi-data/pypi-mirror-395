# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .company_search_result import CompanySearchResult

__all__ = ["SearchIndexResponse", "Pagination"]


class Pagination(BaseModel):
    has_more: bool = FieldInfo(alias="hasMore")

    limit: int

    page: int


class SearchIndexResponse(BaseModel):
    pagination: Pagination
    """Pagination information for search results."""

    search_results: List[CompanySearchResult] = FieldInfo(alias="searchResults")
