# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .identifier import Identifier

__all__ = ["SearchAutocompleteResponse", "Result"]


class Result(BaseModel):
    jurisdiction_code: str = FieldInfo(alias="jurisdictionCode")
    """ISO 3166-1 alpha-2 country code"""

    kausate_id: str = FieldInfo(alias="kausateId")

    name: str

    alternative_names: Optional[str] = FieldInfo(alias="alternativeNames", default=None)
    """Alternative name that matched the search query, if applicable"""

    identifiers: Optional[List[Identifier]] = None
    """List of identifiers for autocomplete display (register numbers, IDs, etc.)"""


class SearchAutocompleteResponse(BaseModel):
    results: List[Result]
