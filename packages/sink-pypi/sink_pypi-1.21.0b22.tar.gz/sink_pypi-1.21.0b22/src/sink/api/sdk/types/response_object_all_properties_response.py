# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from .._models import BaseModel
from .simple_allof import SimpleAllof
from .company.company_payment import CompanyPayment

__all__ = ["ResponseObjectAllPropertiesResponse"]


class ResponseObjectAllPropertiesResponse(BaseModel):
    allof: SimpleAllof

    b: bool

    e: Literal["active", "inactive", "pending"]

    f: float

    i: int

    n: None = None

    object_array: List[CompanyPayment]

    primitive_array: List[str]

    s: str
