# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Role"]


class Role(BaseModel):
    english_translation: Optional[str] = FieldInfo(alias="englishTranslation", default=None)

    iso5009_role_code: Optional[str] = FieldInfo(alias="iso5009RoleCode", default=None)

    original: Optional[str] = None
