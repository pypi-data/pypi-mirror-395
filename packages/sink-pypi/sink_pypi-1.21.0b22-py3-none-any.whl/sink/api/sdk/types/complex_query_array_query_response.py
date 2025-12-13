# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ComplexQueryArrayQueryResponse"]


class ComplexQueryArrayQueryResponse(BaseModel):
    include: List[Literal["users", "users.comments", "users.posts"]]
