# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "StreamingNestedParamsParamsBase",
    "ParentObject",
    "ParentObjectArrayProp",
    "ParentObjectChildProp",
    "StreamingNestedParamsParamsNonStreaming",
    "StreamingNestedParamsParamsStreaming",
]


class StreamingNestedParamsParamsBase(TypedDict, total=False):
    model: Required[str]

    prompt: Required[str]

    parent_object: ParentObject


class ParentObjectArrayProp(TypedDict, total=False):
    from_array_items: bool


class ParentObjectChildProp(TypedDict, total=False):
    from_object: str


class ParentObject(TypedDict, total=False):
    array_prop: Iterable[ParentObjectArrayProp]

    child_prop: ParentObjectChildProp


class StreamingNestedParamsParamsNonStreaming(StreamingNestedParamsParamsBase, total=False):
    stream: Literal[False]


class StreamingNestedParamsParamsStreaming(StreamingNestedParamsParamsBase):
    stream: Required[Literal[True]]


StreamingNestedParamsParams = Union[StreamingNestedParamsParamsNonStreaming, StreamingNestedParamsParamsStreaming]
