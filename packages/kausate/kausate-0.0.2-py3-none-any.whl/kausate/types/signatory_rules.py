# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["SignatoryRules"]


class SignatoryRules(BaseModel):
    english_translation: Optional[str] = FieldInfo(alias="englishTranslation", default=None)

    original: Optional[str] = None
