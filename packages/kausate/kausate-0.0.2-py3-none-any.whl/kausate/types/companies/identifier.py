# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ..._models import BaseModel

__all__ = ["Identifier"]


class Identifier(BaseModel):
    type: str
    """The type must include the jurisdiction in which it is issued"""

    value: str
    """The text/number value of the identifier"""

    description: Optional[str] = None
    """
    Free-text description of the identifier when type is unknown or needs
    clarification
    """

    extra: Optional[Dict[str, object]] = None
    """Additional metadata about the identifier"""

    source: Optional[str] = None
    """The source of this identifier (e.g., 'registrar', 'company', 'third_party')"""
