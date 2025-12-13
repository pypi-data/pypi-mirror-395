# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Required, TypeAlias, TypedDict

from .union_discriminated_variant_a_param import UnionDiscriminatedVariantAParam
from .union_discriminated_variant_b_param import UnionDiscriminatedVariantBParam

__all__ = ["UnionArrayParamDiscriminatedByPropertyNameParams", "Body"]


class UnionArrayParamDiscriminatedByPropertyNameParams(TypedDict, total=False):
    body: Required[Iterable[Body]]


Body: TypeAlias = Union[UnionDiscriminatedVariantAParam, UnionDiscriminatedVariantBParam]
