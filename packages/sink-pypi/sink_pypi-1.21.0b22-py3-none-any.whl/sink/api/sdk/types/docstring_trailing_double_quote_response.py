# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["DocstringTrailingDoubleQuoteResponse"]


class DocstringTrailingDoubleQuoteResponse(BaseModel):
    prop: bool
    """This description ends in a " """

    prop2: bool
    """This description ends in a \" """

    prop3: bool
    """This description ends in a \\" """
