# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["GermanAdvancedQueryParam"]


class GermanAdvancedQueryParam(TypedDict, total=False):
    court_city: Annotated[Optional[str], PropertyInfo(alias="courtCity")]
    """Court city name (e.g., 'München', 'Berlin').

    Will be fuzzy-matched and converted to courtId. Cannot be used with courtId.
    Empty string treated as None.
    """

    court_id: Annotated[Optional[str], PropertyInfo(alias="courtId")]
    """Court ID (e.g., 'D2803', 'D2601').

    Cannot be used with courtCity. Empty string treated as None.
    """

    jurisdiction: Literal["de"]
    """
    Jurisdiction discriminator (automatically inferred from jurisdictionCode at API
    level)
    """

    name: Optional[str]
    """Company name to search for.

    Can be used alone or combined with identifier fields for more specific searches.
    Empty string treated as None.
    """

    register_number: Annotated[Union[str, int, None], PropertyInfo(alias="registerNumber")]
    """Register number (e.g., '10364B', '10364', 10364, 'HRB 275800', or 'HR B
    275800').

    Can include register type prefix (HRB, HRA, HR B, HR A, G NR, etc.) which will
    be automatically extracted and used if registerType is not explicitly provided.
    Supports both spaced (HR B) and non-spaced (HRB) variants. If string contains
    suffix, it will be extracted.
    """

    register_suffix: Annotated[Optional[str], PropertyInfo(alias="registerSuffix")]
    """Register suffix (e.g., 'B', 'BHV').

    Can be provided explicitly or extracted from registerNumber. Case-insensitive -
    will be normalized to uppercase. Empty string treated as None.
    """

    register_type: Annotated[Optional[str], PropertyInfo(alias="registerType")]
    """Register type (e.g., 'HRB', 'HRA', 'GNR', 'PR', 'VR').

    Case-insensitive - will be normalized to uppercase. Empty string treated as
    None.
    """
