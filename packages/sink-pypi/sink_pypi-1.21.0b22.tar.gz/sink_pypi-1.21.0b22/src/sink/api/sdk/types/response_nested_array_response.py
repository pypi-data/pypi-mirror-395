# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["ResponseNestedArrayResponse", "Object"]


class Object(BaseModel):
    bar: Optional[float] = None

    foo: Optional[str] = None


class ResponseNestedArrayResponse(BaseModel):
    objects: List[Object]
