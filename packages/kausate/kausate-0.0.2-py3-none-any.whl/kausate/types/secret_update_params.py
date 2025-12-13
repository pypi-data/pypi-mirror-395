# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["SecretUpdateParams"]


class SecretUpdateParams(TypedDict, total=False):
    secret_values: Required[Annotated[Dict[str, str], PropertyInfo(alias="secretValues")]]

    partner_customer_id: Annotated[Optional[str], PropertyInfo(alias="partnerCustomerId")]
    """Partner customer ID"""
