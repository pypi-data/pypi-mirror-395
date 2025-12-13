# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["HeaderParamArraysParams"]


class HeaderParamArraysParams(TypedDict, total=False):
    x_required_int_array: Required[Annotated[Iterable[int], PropertyInfo(alias="X-Required-Int-Array")]]

    x_required_string_array: Required[Annotated[SequenceNotStr[str], PropertyInfo(alias="X-Required-String-Array")]]

    body_argument: str

    x_optional_int_array: Annotated[Iterable[int], PropertyInfo(alias="X-Optional-Int-Array")]

    x_optional_string_array: Annotated[SequenceNotStr[str], PropertyInfo(alias="X-Optional-String-Array")]
