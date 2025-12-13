# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["DocumentResult"]


class DocumentResult(BaseModel):
    content_type: Optional[str] = FieldInfo(alias="contentType", default=None)

    document_type: Optional[str] = FieldInfo(alias="documentType", default=None)

    download_link: Optional[str] = FieldInfo(alias="downloadLink", default=None)

    expires_at: Optional[str] = FieldInfo(alias="expiresAt", default=None)

    file_name: Optional[str] = FieldInfo(alias="fileName", default=None)

    kausate_document_id: Optional[str] = FieldInfo(alias="kausateDocumentId", default=None)

    type: Optional[Literal["document"]] = None
