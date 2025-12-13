# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ReservedNameCommonReservedParamsParams"]


class ReservedNameCommonReservedParamsParams(TypedDict, total=False):
    from_: Required[Annotated[str, PropertyInfo(alias="from")]]

    api_self: Required[Annotated[int, PropertyInfo(alias="self")]]
