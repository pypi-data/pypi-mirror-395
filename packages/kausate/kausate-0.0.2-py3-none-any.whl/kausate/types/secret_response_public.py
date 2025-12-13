# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["SecretResponsePublic"]


class SecretResponsePublic(BaseModel):
    created_at: datetime = FieldInfo(alias="createdAt")

    datasource_name: str = FieldInfo(alias="datasourceName")

    datasource_slug: str = FieldInfo(alias="datasourceSlug")

    updated_at: datetime = FieldInfo(alias="updatedAt")
