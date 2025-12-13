# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["CursorListReverseParams"]


class CursorListReverseParams(TypedDict, total=False):
    after_id: Optional[str]
    """ID of the object to use as a cursor for pagination.

    When provided, returns the page of results immediately after this object.
    """

    before_id: Optional[str]
    """ID of the object to use as a cursor for pagination.

    When provided, returns the page of results immediately before this object.
    """

    limit: int
