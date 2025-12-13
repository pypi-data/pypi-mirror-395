# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["CompanyReport"]


class CompanyReport(BaseModel):
    company_report: CompanyReport = FieldInfo(alias="companyReport")

    type: Optional[Literal["companyReport"]] = None
