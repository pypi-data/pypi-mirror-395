# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["UltimateBeneficialOwnerReport"]


class UltimateBeneficialOwnerReport(BaseModel):
    ultimate_beneficial_owner_report: UltimateBeneficialOwnerReport = FieldInfo(alias="ultimateBeneficialOwnerReport")

    type: Optional[Literal["uboReport"]] = None
