# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["DocstringLeadingDoubleQuoteResponse"]


class DocstringLeadingDoubleQuoteResponse(BaseModel):
    prop: bool
    """\"This description starts with a double quote"""
