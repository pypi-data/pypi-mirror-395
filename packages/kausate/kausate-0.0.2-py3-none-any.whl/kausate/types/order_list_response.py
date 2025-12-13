# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["OrderListResponse", "Order"]


class Order(BaseModel):
    order_id: str = FieldInfo(alias="orderId")

    request_time: datetime = FieldInfo(alias="requestTime")
    """Time when the order was created"""

    status: str
    """Order status"""

    company_name: Optional[str] = FieldInfo(alias="companyName", default=None)
    """Company name from search attributes"""

    customer_reference: Optional[str] = FieldInfo(alias="customerReference", default=None)

    partner_customer_id: Optional[str] = FieldInfo(alias="partnerCustomerId", default=None)

    response_time: Optional[datetime] = FieldInfo(alias="responseTime", default=None)
    """Time when the order completed"""


class OrderListResponse(BaseModel):
    orders: List[Order]
    """List of orders"""

    total: int
    """Total number of orders returned"""
