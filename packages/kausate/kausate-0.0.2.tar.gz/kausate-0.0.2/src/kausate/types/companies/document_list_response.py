# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from ..product_order_response import ProductOrderResponse

__all__ = ["DocumentListResponse", "ListDocumentsResponse", "ListDocumentsResponseDocument"]


class ListDocumentsResponseDocument(BaseModel):
    kausate_document_id: str = FieldInfo(alias="kausateDocumentId")
    """Stable document ID for download requests"""

    title: str
    """Full title of the document"""

    document_type: Optional[str] = FieldInfo(alias="documentType", default=None)
    """Document type (annualAccounts, currentExtract, shareholderList, etc.)"""

    file_type: Optional[str] = FieldInfo(alias="fileType", default=None)
    """File format/extension (pdf, xml, etc.)"""

    publication_date: Optional[str] = FieldInfo(alias="publicationDate", default=None)
    """Date when the document was published (ISO format)"""

    publication_type: Optional[str] = FieldInfo(alias="publicationType", default=None)
    """Publication type name from the source register"""

    source: Optional[str] = None
    """Source register of the document"""


class ListDocumentsResponse(BaseModel):
    documents: List[ListDocumentsResponseDocument]
    """List of available documents"""

    kausate_id: str = FieldInfo(alias="kausateId")
    """Kausate company identifier"""

    total_count: int = FieldInfo(alias="totalCount")
    """Total number of documents found"""

    expires_at: Optional[datetime] = FieldInfo(alias="expiresAt", default=None)
    """Timestamp when the index expires"""

    indexed_at: Optional[datetime] = FieldInfo(alias="indexedAt", default=None)
    """Timestamp when the documents were indexed"""


DocumentListResponse: TypeAlias = Union[ProductOrderResponse, ListDocumentsResponse]
