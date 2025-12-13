# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import TypeAlias

from .product_order_response import ProductOrderResponse
from .ultimate_beneficial_owner_report import UltimateBeneficialOwnerReport

__all__ = ["CompanyExtractUboResponse"]

CompanyExtractUboResponse: TypeAlias = Union[ProductOrderResponse, UltimateBeneficialOwnerReport]
