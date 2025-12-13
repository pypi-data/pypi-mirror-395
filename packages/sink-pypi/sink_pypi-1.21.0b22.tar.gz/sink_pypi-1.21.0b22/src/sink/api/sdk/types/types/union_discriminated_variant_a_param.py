# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["UnionDiscriminatedVariantAParam"]


class UnionDiscriminatedVariantAParam(TypedDict, total=False):
    value: Required[str]

    type: Literal["a"]
