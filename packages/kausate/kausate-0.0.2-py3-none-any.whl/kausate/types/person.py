# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .date_info import DateInfo
from .companies.address import Address
from .companies.identifier import Identifier

__all__ = ["Person", "Name"]


class Name(BaseModel):
    first_name: Optional[str] = FieldInfo(alias="firstName", default=None)

    full_name: Optional[str] = FieldInfo(alias="fullName", default=None)

    last_name: Optional[str] = FieldInfo(alias="lastName", default=None)


class Person(BaseModel):
    address: Optional[Address] = None
    """Address of a company or person."""

    contact: Optional[Dict[str, str]] = None

    date_of_birth: Optional[DateInfo] = FieldInfo(alias="dateOfBirth", default=None)

    gender: Optional[str] = None

    identifiers: Optional[List[Identifier]] = None

    jurisdiction_code: Optional[str] = FieldInfo(alias="jurisdictionCode", default=None)
    """ISO 3166-1 alpha-2 country/jurisdiction code"""

    name: Optional[Name] = None

    nationality: Optional[str] = None
