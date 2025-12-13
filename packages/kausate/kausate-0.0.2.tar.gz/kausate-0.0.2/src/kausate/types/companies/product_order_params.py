# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ProductOrderParams"]


class ProductOrderParams(TypedDict, total=False):
    sync: bool
    """Return result synchronously with 300s timeout"""

    customer_reference: Annotated[Optional[str], PropertyInfo(alias="customerReference")]

    kausate_document_id: Annotated[Optional[str], PropertyInfo(alias="kausateDocumentId")]
    """Document ID from /documents/list response (e.g., doc_deur_abc123).

    Required if sku not provided.
    """

    output_format: Annotated[Literal["pdf", "raw"], PropertyInfo(alias="outputFormat")]
    """Output format.

    'pdf' converts TIFF files to PDF (default). 'raw' keeps original format.
    """

    sku: Optional[str]
    """Product SKU code (e.g., DEHRAD, DEHRSI).

    Required if kausateDocumentId not provided.
    """

    x_partner_customer_id: Annotated[str, PropertyInfo(alias="X-Partner-Customer-Id")]
    """Optional partner customer ID"""
