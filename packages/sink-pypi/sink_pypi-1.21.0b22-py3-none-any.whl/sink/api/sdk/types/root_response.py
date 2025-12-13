# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["RootResponse"]


class RootResponse(BaseModel):
    check_escaping: Literal[
        "And now, a set of characters that are likely to cause issues if not properly escaped:\n- quotes: \" ' ` - slashes: / // /// \\ \\\\ \\\\\\ - others: \\n \\r \\t \\b \\f \\v \\x63 \\uFE63 \\U0000FE63 \\N{HYPHEN} \\1 \\12 \\123 \\1234 a \\a \\g \\* \\( \\& \\@ \\x2z \\u11z1 \\U1111z111 \\N{HYPHEN#} ${test} #{test}\n"
    ] = FieldInfo(alias="checkEscaping")

    message: str
