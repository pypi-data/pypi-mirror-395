# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["ComplexQueryArrayQueryParams"]


class ComplexQueryArrayQueryParams(TypedDict, total=False):
    include: List[Literal["users", "users.comments", "users.posts"]]
