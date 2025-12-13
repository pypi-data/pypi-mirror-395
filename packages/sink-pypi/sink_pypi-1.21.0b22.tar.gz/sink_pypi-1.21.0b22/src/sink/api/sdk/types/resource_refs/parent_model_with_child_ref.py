# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel
from .parent.child_model import ChildModel

__all__ = ["ParentModelWithChildRef"]


class ParentModelWithChildRef(BaseModel):
    from_array: List[ChildModel]

    from_prop: ChildModel

    string_prop: Optional[str] = None
