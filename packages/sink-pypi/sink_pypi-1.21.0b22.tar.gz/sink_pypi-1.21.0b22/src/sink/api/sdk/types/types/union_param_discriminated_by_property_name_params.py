# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["UnionParamDiscriminatedByPropertyNameParams", "UnionDiscriminatedVariantA", "UnionDiscriminatedVariantB"]


class UnionDiscriminatedVariantA(TypedDict, total=False):
    value: Required[str]

    type: Literal["a"]


class UnionDiscriminatedVariantB(TypedDict, total=False):
    value: Required[str]

    type: Literal["b"]


UnionParamDiscriminatedByPropertyNameParams: TypeAlias = Union[UnionDiscriminatedVariantA, UnionDiscriminatedVariantB]
