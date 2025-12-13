# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["QueryParamObjectParams", "ObjectParam", "ObjectRefParam"]


class QueryParamObjectParams(TypedDict, total=False):
    object_param: ObjectParam

    object_ref_param: ObjectRefParam


class ObjectParam(TypedDict, total=False):
    foo: str


class ObjectRefParam(TypedDict, total=False):
    item: str
