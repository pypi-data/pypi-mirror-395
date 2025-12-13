# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import builtins
import datetime
from typing import Union
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["NamePropertiesCommonConflictsParams"]


class NamePropertiesCommonConflictsParams(TypedDict, total=False):
    _1_digit_leading_underscore: Required[str]
    """
    In certain languages the leading underscore in combination with this property
    name may cause issues
    """

    _leading_underscore: Required[str]
    """
    In certain languages the leading underscore in this property name may cause
    issues
    """

    _leading_underscore_mixed_case: Required[Annotated[str, PropertyInfo(alias="_leading_underscore_MixedCase")]]
    """
    In certain languages the leading underscore in this property name may cause
    issues alongside a case change
    """

    bool: Required[builtins.bool]

    bool_2: Required[builtins.bool]
    """
    In certain languages the type declaration for this prop can shadow the `bool`
    property declaration.
    """

    date: Required[Annotated[Union[str, datetime.date], PropertyInfo(format="iso8601")]]
    """This shadows the stdlib `datetime.date` type in Python & causes type errors."""

    date_2: Required[Annotated[Union[str, datetime.date], PropertyInfo(format="iso8601")]]
    """
    In certain languages the type declaration for this prop can shadow the `date`
    property declaration.
    """

    float: Required[builtins.float]

    float_2: Required[builtins.float]
    """
    In certain languages the type declaration for this prop can shadow the `float`
    property declaration.
    """

    int: Required[builtins.int]

    int_2: Required[builtins.int]
    """
    In certain languages the type declaration for this prop can shadow the `int`
    property declaration.
    """
