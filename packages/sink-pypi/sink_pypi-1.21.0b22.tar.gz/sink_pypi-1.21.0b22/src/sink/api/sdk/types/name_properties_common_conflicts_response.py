# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["NamePropertiesCommonConflictsResponse"]


class NamePropertiesCommonConflictsResponse(BaseModel):
    api_1_digit_leading_underscore: str = FieldInfo(alias="_1_digit_leading_underscore")
    """
    In certain languages the leading underscore in combination with this property
    name may cause issues
    """

    api_leading_underscore: str = FieldInfo(alias="_leading_underscore")
    """
    In certain languages the leading underscore in this property name may cause
    issues
    """

    api_leading_underscore_mixed_case: str = FieldInfo(alias="_leading_underscore_MixedCase")
    """
    In certain languages the leading underscore in this property name may cause
    issues alongside a case change
    """

    bool: builtins.bool

    bool_2: builtins.bool
    """
    In certain languages the type declaration for this prop can shadow the `bool`
    property declaration.
    """

    date: datetime.date
    """This shadows the stdlib `datetime.date` type in Python & causes type errors."""

    date_2: datetime.date
    """
    In certain languages the type declaration for this prop can shadow the `date`
    property declaration.
    """

    float: builtins.float

    float_2: builtins.float
    """
    In certain languages the type declaration for this prop can shadow the `float`
    property declaration.
    """

    int: builtins.int

    int_2: builtins.int
    """
    In certain languages the type declaration for this prop can shadow the `int`
    property declaration.
    """
