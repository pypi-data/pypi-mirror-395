# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["TypeDatetimesParams"]


class TypeDatetimesParams(TypedDict, total=False):
    required_datetime: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    required_nullable_datetime: Required[Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]]

    list_datetime: Annotated[SequenceNotStr[Union[str, datetime]], PropertyInfo(format="iso8601")]

    oneof_datetime: Annotated[Union[Union[str, datetime], int], PropertyInfo(format="iso8601")]
    """union type coming from the `oneof_datetime` property"""

    optional_datetime: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
