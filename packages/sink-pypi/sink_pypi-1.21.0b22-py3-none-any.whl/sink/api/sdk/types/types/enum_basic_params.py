# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

from ..shared.currency import Currency

__all__ = ["EnumBasicParams"]


class EnumBasicParams(TypedDict, total=False):
    input_currency: Currency
    """This is my description for the Currency enum"""

    problematic_enum: Literal["123_FOO", "30%", "*", ""]

    uses_const: Literal["my_const_enum_value"]
