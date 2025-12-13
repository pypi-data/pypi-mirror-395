# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["PositionalParamMultiplePathParamsParams"]


class PositionalParamMultiplePathParamsParams(TypedDict, total=False):
    first: Required[str]

    last: Required[str]

    name: Required[str]

    options: str
