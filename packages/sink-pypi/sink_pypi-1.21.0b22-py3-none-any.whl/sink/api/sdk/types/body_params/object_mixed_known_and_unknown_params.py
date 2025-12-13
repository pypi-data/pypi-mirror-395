# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import TypeAlias, TypedDict

__all__ = ["ObjectMixedKnownAndUnknownParams", "MixedProp"]


class ObjectMixedKnownAndUnknownParams(TypedDict, total=False):
    mixed_prop: MixedProp


class MixedPropTyped(TypedDict, total=False):
    my_known_prop: int


MixedProp: TypeAlias = Union[MixedPropTyped, Dict[str, str]]
