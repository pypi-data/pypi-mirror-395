# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypedDict

__all__ = ["StreamingBasicParamsBase", "StreamingBasicParamsNonStreaming", "StreamingBasicParamsStreaming"]


class StreamingBasicParamsBase(TypedDict, total=False):
    model: Required[str]

    prompt: Required[str]


class StreamingBasicParamsNonStreaming(StreamingBasicParamsBase, total=False):
    stream: Literal[False]


class StreamingBasicParamsStreaming(StreamingBasicParamsBase):
    stream: Required[Literal[True]]


StreamingBasicParams = Union[StreamingBasicParamsNonStreaming, StreamingBasicParamsStreaming]
