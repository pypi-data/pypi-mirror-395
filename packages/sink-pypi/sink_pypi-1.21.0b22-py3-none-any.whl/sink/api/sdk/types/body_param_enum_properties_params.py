# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["BodyParamEnumPropertiesParams"]


class BodyParamEnumPropertiesParams(TypedDict, total=False):
    code: Literal[1, 2]

    enabled: Literal[True]

    kind: Literal["failed", "success"]
