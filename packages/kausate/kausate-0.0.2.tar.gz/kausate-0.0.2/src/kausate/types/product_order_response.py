# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ProductOrderResponse"]


class ProductOrderResponse(BaseModel):
    order_id: str = FieldInfo(alias="orderId")

    customer_reference: Optional[str] = FieldInfo(alias="customerReference", default=None)

    partner_customer_id: Optional[str] = FieldInfo(alias="partnerCustomerId", default=None)
