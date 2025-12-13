# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "StreamingWithUnrelatedDefaultParamParamsBase",
    "StreamingWithUnrelatedDefaultParamParamsNonStreaming",
    "StreamingWithUnrelatedDefaultParamParamsStreaming",
]


class StreamingWithUnrelatedDefaultParamParamsBase(TypedDict, total=False):
    model: Required[str]

    param_with_default_value: Literal["my_enum_value"]

    prompt: Required[str]


class StreamingWithUnrelatedDefaultParamParamsNonStreaming(StreamingWithUnrelatedDefaultParamParamsBase, total=False):
    stream: Literal[False]


class StreamingWithUnrelatedDefaultParamParamsStreaming(StreamingWithUnrelatedDefaultParamParamsBase):
    stream: Required[Literal[True]]


StreamingWithUnrelatedDefaultParamParams = Union[
    StreamingWithUnrelatedDefaultParamParamsNonStreaming, StreamingWithUnrelatedDefaultParamParamsStreaming
]
