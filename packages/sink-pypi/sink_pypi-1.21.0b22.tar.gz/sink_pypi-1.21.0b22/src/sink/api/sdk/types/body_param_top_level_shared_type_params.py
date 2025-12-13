# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .shared_params.simple_object import SimpleObject

__all__ = ["BodyParamTopLevelSharedTypeParams"]


class BodyParamTopLevelSharedTypeParams(TypedDict, total=False):
    bar: SimpleObject

    foo: str
