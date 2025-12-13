# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["HeaderParamAllTypesParams"]


class HeaderParamAllTypesParams(TypedDict, total=False):
    x_required_boolean: Required[Annotated[bool, PropertyInfo(alias="X-Required-Boolean")]]

    x_required_integer: Required[Annotated[int, PropertyInfo(alias="X-Required-Integer")]]

    x_required_number: Required[Annotated[float, PropertyInfo(alias="X-Required-Number")]]

    x_required_string: Required[Annotated[str, PropertyInfo(alias="X-Required-String")]]

    body_argument: str

    x_nullable_integer: Annotated[int, PropertyInfo(alias="X-Nullable-Integer")]

    x_optional_boolean: Annotated[bool, PropertyInfo(alias="X-Optional-Boolean")]

    x_optional_integer: Annotated[int, PropertyInfo(alias="X-Optional-Integer")]

    x_optional_number: Annotated[float, PropertyInfo(alias="X-Optional-Number")]

    x_optional_string: Annotated[str, PropertyInfo(alias="X-Optional-String")]
