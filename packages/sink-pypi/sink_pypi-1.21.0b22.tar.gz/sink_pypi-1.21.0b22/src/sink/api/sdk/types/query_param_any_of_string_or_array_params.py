# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypedDict

from .._types import SequenceNotStr

__all__ = ["QueryParamAnyOfStringOrArrayParams"]


class QueryParamAnyOfStringOrArrayParams(TypedDict, total=False):
    ids: Union[str, SequenceNotStr[str]]
