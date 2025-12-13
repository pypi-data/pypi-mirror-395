# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import TypeAlias

from .live_search_response import LiveSearchResponse
from ..product_order_response import ProductOrderResponse

__all__ = ["SearchRealTimeResponse"]

SearchRealTimeResponse: TypeAlias = Union[LiveSearchResponse, ProductOrderResponse]
