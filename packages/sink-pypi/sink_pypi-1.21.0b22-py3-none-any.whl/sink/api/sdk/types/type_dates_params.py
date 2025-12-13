# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import date
from typing_extensions import Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["TypeDatesParams"]


class TypeDatesParams(TypedDict, total=False):
    required_date: Required[Annotated[Union[str, date], PropertyInfo(format="iso8601")]]

    required_nullable_date: Required[Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]]

    list_date: Annotated[SequenceNotStr[Union[str, date]], PropertyInfo(format="iso8601")]

    oneof_date: Annotated[Union[Union[str, date], int], PropertyInfo(format="iso8601")]

    optional_date: Annotated[Union[str, date], PropertyInfo(format="iso8601")]
