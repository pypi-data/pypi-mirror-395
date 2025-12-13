# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .role import Role
from .person import Person
from .status import Status
from .._models import BaseModel
from .currency import Currency
from .legal_form import LegalForm
from .interest_type import InterestType
from .percentage_share import PercentageShare
from .companies.address import Address
from .companies.identifier import Identifier

__all__ = ["Shareholder", "Company"]


class Company(BaseModel):
    address: Optional[Address] = None
    """Address of a company or person."""

    identifiers: Optional[List[Identifier]] = None

    jurisdiction_code: Optional[str] = FieldInfo(alias="jurisdictionCode", default=None)
    """ISO 3166-1 alpha-2 country/jurisdiction code"""

    legal_form: Optional[LegalForm] = FieldInfo(alias="legalForm", default=None)

    name: Optional[str] = None

    status: Optional[Status] = None


class Shareholder(BaseModel):
    type: Literal["person", "company", "freeFloat"]
    """Type of shareholder"""

    company: Optional[Company] = None
    """A legal entity or organization"""

    description: Optional[str] = None

    interest_details: Optional[str] = FieldInfo(alias="interestDetails", default=None)
    """
    Additional details about the interest, such as the specific role name (e.g.,
    'Komplementär')
    """

    interest_type: Optional[InterestType] = FieldInfo(alias="interestType", default=None)
    """
    Describes the nature of the interest or control that an entity or person has in
    another entity.
    """

    number_of_shares: Optional[int] = FieldInfo(alias="numberOfShares", default=None)

    percentage: Optional[PercentageShare] = None
    """
    The proportion of this type of interest held by the interested party, where an
    interest is countable.
    """

    person: Optional[Person] = None
    """A natural person (human being)"""

    role: Optional[Role] = None

    share_class: Optional[str] = FieldInfo(alias="shareClass", default=None)

    source: Optional[str] = None

    total_nominal_value: Optional[Currency] = FieldInfo(alias="totalNominalValue", default=None)
