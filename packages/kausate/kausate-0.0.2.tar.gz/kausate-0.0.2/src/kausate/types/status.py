# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Status"]


class Status(BaseModel):
    is_active: Optional[bool] = FieldInfo(alias="isActive", default=None)

    normalized: Optional[
        Literal[
            "active",
            "closed",
            "closing",
            "dissolved",
            "expanded",
            "expired",
            "inReceivership",
            "inactive",
            "incorporated",
            "opening",
            "registered",
            "registrationRevoked",
            "seized",
            "terminated",
            "underExternalControl",
        ]
    ] = None
    """Company status type definitions with descriptions"""

    original: Optional[str] = None
