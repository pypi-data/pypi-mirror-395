# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["EnumArrayUniqueValuesNumbersParams"]


class EnumArrayUniqueValuesNumbersParams(TypedDict, total=False):
    body: Required[Iterable[Literal[5, 6, 7, 8, 9]]]
