# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import TypeAlias

from ..company_report import CompanyReport
from ..product_order_response import ProductOrderResponse

__all__ = ["ReportCreateResponse"]

ReportCreateResponse: TypeAlias = Union[ProductOrderResponse, CompanyReport]
