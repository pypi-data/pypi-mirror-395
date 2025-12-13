# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel
from ..shared.currency import Currency

__all__ = ["EnumBasicResponse"]


class EnumBasicResponse(BaseModel):
    currency: Currency
    """This is my description for the Currency enum"""

    enum_with_dupes: Literal["user", "assistant"]

    my_problematic_enum: Literal["123_FOO", "30%", "*", ""]

    number_enum: Literal[200, 201, 404, 403]

    uses_const: Literal["my_const_enum_value"]
