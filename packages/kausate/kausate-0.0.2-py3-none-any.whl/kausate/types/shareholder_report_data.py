# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .date_info import DateInfo
from .shareholder import Shareholder

__all__ = ["ShareholderReportData", "Sources"]


class Sources(BaseModel):
    type: Literal["selfDeclaration", "officialRegister", "thirdParty", "primaryResearch", "verified"]
    """Source type for information origin."""

    date: Optional[DateInfo] = None

    download_url: Optional[str] = FieldInfo(alias="downloadUrl", default=None)

    file_hash: Optional[str] = FieldInfo(alias="fileHash", default=None)

    file_name: Optional[str] = FieldInfo(alias="fileName", default=None)

    jurisdiction_code: Optional[str] = FieldInfo(alias="jurisdictionCode", default=None)

    name: Optional[str] = None

    retrieval_time: Optional[str] = FieldInfo(alias="retrievalTime", default=None)


class ShareholderReportData(BaseModel):
    shareholders: Optional[List[Shareholder]] = None

    sources: Optional[Dict[str, Sources]] = None
