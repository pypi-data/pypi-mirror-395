# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["SearchAutocompleteParams"]


class SearchAutocompleteParams(TypedDict, total=False):
    query: Required[str]

    jurisdiction_code: Annotated[Optional[str], PropertyInfo(alias="jurisdictionCode")]

    limit: Optional[int]
