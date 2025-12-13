# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel
from .basic_shared_model_object import BasicSharedModelObject

__all__ = ["PageCursorSharedRefPagination"]


class PageCursorSharedRefPagination(BaseModel):
    cursor: str

    prop_with_another_ref: Optional[BasicSharedModelObject] = None
