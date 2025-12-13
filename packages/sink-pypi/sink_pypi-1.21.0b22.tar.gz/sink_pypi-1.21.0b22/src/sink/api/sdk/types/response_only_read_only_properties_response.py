# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .shared.currency import Currency

__all__ = ["ResponseOnlyReadOnlyPropertiesResponse"]


class ResponseOnlyReadOnlyPropertiesResponse(BaseModel):
    read_only_enum: Currency
    """This is my description for the Currency enum"""

    read_only_property: str
