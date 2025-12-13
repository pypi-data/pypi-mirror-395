# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "StreamingQueryParamDiscriminatorParamsBase",
    "StreamingQueryParamDiscriminatorParamsNonStreaming",
    "StreamingQueryParamDiscriminatorParamsStreaming",
]


class StreamingQueryParamDiscriminatorParamsBase(TypedDict, total=False):
    prompt: Required[str]


class StreamingQueryParamDiscriminatorParamsNonStreaming(StreamingQueryParamDiscriminatorParamsBase, total=False):
    should_stream: Literal[False]


class StreamingQueryParamDiscriminatorParamsStreaming(StreamingQueryParamDiscriminatorParamsBase):
    should_stream: Required[Literal[True]]


StreamingQueryParamDiscriminatorParams = Union[
    StreamingQueryParamDiscriminatorParamsNonStreaming, StreamingQueryParamDiscriminatorParamsStreaming
]
