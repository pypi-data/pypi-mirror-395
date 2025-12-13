# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

__all__ = [
    "NamePropertiesIllegalJavascriptIdentifiersParams",
    "_2llegalJavascriptIdentifiers",
    "_3llegalJavascriptIdentifiers",
]


class _2llegalJavascriptIdentifiers(TypedDict, total=False):
    irrelevant: float


class _3llegalJavascriptIdentifiers(TypedDict, total=False):
    body: Required[float]


NamePropertiesIllegalJavascriptIdentifiersParams: TypeAlias = Union[
    _2llegalJavascriptIdentifiers, _3llegalJavascriptIdentifiers
]
