# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .address import Address
from ..._models import BaseModel
from .identifier import Identifier

__all__ = ["CompanySearchResult"]


class CompanySearchResult(BaseModel):
    jurisdiction_code: str = FieldInfo(alias="jurisdictionCode")
    """ISO 3166-1 alpha-2 country code"""

    kausate_id: str = FieldInfo(alias="kausateId")

    name: str

    addresses: Optional[List[Address]] = None
    """Company addresses (registered office, business addresses, etc.)"""

    alternative_names: Optional[List[str]] = FieldInfo(alias="alternativeNames", default=None)
    """All alternative names (former names) for this company from the index"""

    identifiers: Optional[List[Identifier]] = None
    """Company identifiers (e.g., HR number for German companies)"""
