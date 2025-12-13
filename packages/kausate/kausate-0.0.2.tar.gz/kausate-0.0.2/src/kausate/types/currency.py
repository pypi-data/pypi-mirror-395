# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Currency"]


class Currency(BaseModel):
    amount: Optional[str] = None

    iso4217_currency_code: Optional[str] = FieldInfo(alias="iso4217CurrencyCode", default=None)
    """Currency code in ISO 4217 format"""
