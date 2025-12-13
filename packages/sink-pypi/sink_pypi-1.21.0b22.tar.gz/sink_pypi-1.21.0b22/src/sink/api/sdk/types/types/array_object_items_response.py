# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from ..._models import BaseModel

__all__ = ["ArrayObjectItemsResponse", "ArrayObjectItemsResponseItem"]


class ArrayObjectItemsResponseItem(BaseModel):
    nice_foo: Optional[str] = None


ArrayObjectItemsResponse: TypeAlias = List[ArrayObjectItemsResponseItem]
