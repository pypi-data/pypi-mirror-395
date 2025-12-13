# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["DateInfo"]


class DateInfo(BaseModel):
    normalized: Optional[str] = None

    original: Optional[str] = None
