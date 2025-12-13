# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["OrderListParams"]


class OrderListParams(TypedDict, total=False):
    limit: int
    """Maximum number of orders to return"""

    workflow_type: Annotated[
        Optional[Literal["DocumentRetrieval", "CompanyReport", "ShareholderGraph", "UBOExtraction"]],
        PropertyInfo(alias="workflowType"),
    ]
    """Available workflow types for filtering orders."""
