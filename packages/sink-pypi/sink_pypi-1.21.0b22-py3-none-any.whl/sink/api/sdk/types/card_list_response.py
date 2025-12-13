# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .card import Card
from .._models import BaseModel

__all__ = ["CardListResponse"]


class CardListResponse(BaseModel):
    data: List[Card]

    page: int
    """Page number."""

    total_entries: int
    """Total number of entries."""

    total_pages: int
    """Total number of pages."""
