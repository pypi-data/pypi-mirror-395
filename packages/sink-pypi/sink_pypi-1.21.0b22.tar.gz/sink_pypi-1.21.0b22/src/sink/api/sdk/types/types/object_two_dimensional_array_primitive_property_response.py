# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel

__all__ = ["ObjectTwoDimensionalArrayPrimitivePropertyResponse"]


class ObjectTwoDimensionalArrayPrimitivePropertyResponse(BaseModel):
    boolean_prop: List[List[bool]]

    integer_prop: List[List[int]]

    number_prop: List[List[float]]

    string_prop: List[List[str]]
