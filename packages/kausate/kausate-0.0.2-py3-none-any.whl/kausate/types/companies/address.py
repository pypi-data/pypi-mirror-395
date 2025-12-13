# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["Address", "Normalized"]


class Normalized(BaseModel):
    category: Optional[str] = None

    city: Optional[str] = None

    city_district: Optional[str] = FieldInfo(alias="cityDistrict", default=None)

    country: Optional[str] = None

    country_code: Optional[str] = FieldInfo(alias="countryCode", default=None)

    country_region: Optional[str] = FieldInfo(alias="countryRegion", default=None)

    county: Optional[str] = None

    entrance: Optional[str] = None

    house: Optional[str] = None

    house_number: Optional[str] = FieldInfo(alias="houseNumber", default=None)

    island: Optional[str] = None

    level: Optional[str] = None

    near: Optional[str] = None

    po_box: Optional[str] = FieldInfo(alias="poBox", default=None)

    postcode: Optional[str] = None

    road: Optional[str] = None

    staircase: Optional[str] = None

    state: Optional[str] = None

    state_district: Optional[str] = FieldInfo(alias="stateDistrict", default=None)

    suburb: Optional[str] = None

    unit: Optional[str] = None

    world_region: Optional[str] = FieldInfo(alias="worldRegion", default=None)


class Address(BaseModel):
    normalized: Optional[Normalized] = None
    """Normalized address fields with null values excluded from serialization."""

    original: Optional[str] = None

    source: Optional[str] = None

    type: Optional[
        Literal[
            "arrival",
            "business",
            "departure",
            "mailing",
            "operations",
            "physical",
            "placeOfBirth",
            "receiverAddress",
            "registered",
            "residential",
            "shipperAddress",
            "transit",
        ]
    ] = None
    """Address type definitions with descriptions"""
