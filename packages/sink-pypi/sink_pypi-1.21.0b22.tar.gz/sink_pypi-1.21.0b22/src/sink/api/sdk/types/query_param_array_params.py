# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import TypedDict

from .._types import SequenceNotStr

__all__ = ["QueryParamArrayParams"]


class QueryParamArrayParams(TypedDict, total=False):
    integer_array_param: Iterable[int]

    string_array_param: SequenceNotStr[str]
