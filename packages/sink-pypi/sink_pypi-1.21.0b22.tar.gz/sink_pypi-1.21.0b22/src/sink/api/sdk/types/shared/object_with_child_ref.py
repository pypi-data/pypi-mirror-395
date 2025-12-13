# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel
from .simple_object import SimpleObject

__all__ = ["ObjectWithChildRef"]


class ObjectWithChildRef(BaseModel):
    bar: Optional[SimpleObject] = None

    foo: Optional[str] = None
