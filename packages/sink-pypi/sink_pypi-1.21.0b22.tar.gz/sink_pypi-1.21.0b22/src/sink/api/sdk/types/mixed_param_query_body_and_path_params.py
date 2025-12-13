# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["MixedParamQueryBodyAndPathParams"]


class MixedParamQueryBodyAndPathParams(TypedDict, total=False):
    query_param: str
    """Query param description"""

    body_param: str
    """Body param description"""
