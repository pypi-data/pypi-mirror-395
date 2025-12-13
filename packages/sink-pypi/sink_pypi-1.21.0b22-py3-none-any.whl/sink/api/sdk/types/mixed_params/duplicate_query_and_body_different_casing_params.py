# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["DuplicateQueryAndBodyDifferentCasingParams"]


class DuplicateQueryAndBodyDifferentCasingParams(TypedDict, total=False):
    query_correlation_id: Required[Annotated[str, PropertyInfo(alias="correlation-id")]]
    """Query param description"""

    body_correlation_id: Required[Annotated[str, PropertyInfo(alias="correlation_id")]]
    """Body param description"""
