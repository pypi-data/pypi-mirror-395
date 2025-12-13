# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .person import Person
from .._models import BaseModel
from .date_info import DateInfo
from .interest_type import InterestType
from .percentage_share import PercentageShare

__all__ = ["UltimateBeneficialOwner", "Interest"]


class Interest(BaseModel):
    details: Optional[str] = None

    end_date: Optional[DateInfo] = FieldInfo(alias="endDate", default=None)

    percentage: Optional[PercentageShare] = None
    """
    The proportion of this type of interest held by the interested party, where an
    interest is countable.
    """

    start_date: Optional[DateInfo] = FieldInfo(alias="startDate", default=None)

    type: Optional[InterestType] = None
    """
    Describes the nature of the interest or control that an entity or person has in
    another entity.
    """


class UltimateBeneficialOwner(BaseModel):
    interests: Optional[List[Interest]] = None
    """
    The local name given to this kind of interest, or further information
    (semi-structured or unstructured) to clarify the nature of the interest.
    """

    person: Optional[Person] = None
    """A natural person (human being)"""

    source: Optional[str] = None

    type: Optional[Literal["person"]] = None
