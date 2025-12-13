# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["PercentageShare"]


class PercentageShare(BaseModel):
    exact: Optional[float] = None
    """The exact share of this interest held (if available)."""

    exclusive_maximum: Optional[float] = FieldInfo(alias="exclusiveMaximum", default=None)
    """The exclusive upper bound of the share of this interest."""

    exclusive_minimum: Optional[float] = FieldInfo(alias="exclusiveMinimum", default=None)
    """The exclusive lower bound of the share of this interest."""

    maximum: Optional[float] = None
    """The inclusive upper bound of the share of this interest."""

    minimum: Optional[float] = None
    """The inclusive lower bound of the share of this interest."""
