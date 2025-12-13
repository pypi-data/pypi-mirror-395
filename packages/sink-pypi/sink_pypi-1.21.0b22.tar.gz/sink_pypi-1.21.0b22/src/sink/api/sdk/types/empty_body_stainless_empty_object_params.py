# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["EmptyBodyStainlessEmptyObjectParams", "Body"]


class EmptyBodyStainlessEmptyObjectParams(TypedDict, total=False):
    query_param: str
    """Query param description"""

    second_query_param: str
    """Query param description"""

    body: Body


class Body(TypedDict, total=False):
    pass
