# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from datetime import datetime
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from .. import product_order_response
from ..._models import BaseModel
from .document_result import DocumentResult

__all__ = ["ProductOrderResponse", "DownloadDocumentResponse"]


class DownloadDocumentResponse(BaseModel):
    content_type: str = FieldInfo(alias="contentType")
    """MIME type of the document"""

    download_link: str = FieldInfo(alias="downloadLink")
    """URL for downloading the document"""

    expires_at: datetime = FieldInfo(alias="expiresAt")
    """Timestamp when the download URL expires"""

    file_name: str = FieldInfo(alias="fileName")
    """Suggested filename for the download"""

    kausate_document_id: str = FieldInfo(alias="kausateDocumentId")
    """Kausate document ID"""


ProductOrderResponse: TypeAlias = Union[
    product_order_response.ProductOrderResponse, DocumentResult, DownloadDocumentResponse
]
