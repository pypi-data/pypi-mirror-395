# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .company_search_result import CompanySearchResult

__all__ = ["LiveSearchResponse"]


class LiveSearchResponse(BaseModel):
    search_results: List[CompanySearchResult] = FieldInfo(alias="searchResults")

    type: Optional[Literal["liveSearch"]] = None
