# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PositionalParamKitchenSinkParams"]


class PositionalParamKitchenSinkParams(TypedDict, total=False):
    key: Required[str]

    im_a_camel: Required[Annotated[str, PropertyInfo(alias="imACamel")]]

    option1: Required[bool]

    camel_case: Required[str]

    option2: str

    really_cool_snake: str

    bar: float

    options: str

    x_custom_header: Annotated[str, PropertyInfo(alias="X-Custom-Header")]
