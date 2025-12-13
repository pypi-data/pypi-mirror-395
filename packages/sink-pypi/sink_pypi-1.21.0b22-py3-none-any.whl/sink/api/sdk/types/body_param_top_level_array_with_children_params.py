# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

__all__ = ["BodyParamTopLevelArrayWithChildrenParams", "Item"]


class BodyParamTopLevelArrayWithChildrenParams(TypedDict, total=False):
    items: Required[Iterable[Item]]


class Item(TypedDict, total=False):
    id: Required[str]
