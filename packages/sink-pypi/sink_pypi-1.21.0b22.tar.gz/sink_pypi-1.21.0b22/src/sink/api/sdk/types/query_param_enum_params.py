# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

__all__ = ["QueryParamEnumParams"]


class QueryParamEnumParams(TypedDict, total=False):
    integer_enum_param: Literal[100, 200]

    nullable_integer_enum_param: Optional[Literal[100, 200]]

    nullable_number_enum_param: Optional[Literal[100, 200]]

    nullable_string_enum_param: Optional[Literal["foo", "bar"]]

    number_enum_param: Literal[100, 200]

    string_enum_param: Literal["foo", "bar"]
