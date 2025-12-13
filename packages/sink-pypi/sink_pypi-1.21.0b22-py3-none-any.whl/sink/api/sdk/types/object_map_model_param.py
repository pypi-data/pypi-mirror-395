# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypeAlias, TypedDict

__all__ = ["ObjectMapModelParam", "ObjectMapModelParamItem"]


class ObjectMapModelParamItem(TypedDict, total=False):
    foo: str


ObjectMapModelParam: TypeAlias = Dict[str, ObjectMapModelParamItem]
