# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["PositionalParamQueryMultipleParams"]


class PositionalParamQueryMultipleParams(TypedDict, total=False):
    bar: Required[str]
    """Some description about bar."""

    foo: Required[str]
    """Some description about foo."""
