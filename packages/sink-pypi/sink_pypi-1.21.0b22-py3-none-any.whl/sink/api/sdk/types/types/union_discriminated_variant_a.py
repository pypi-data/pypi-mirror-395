# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["UnionDiscriminatedVariantA"]


class UnionDiscriminatedVariantA(BaseModel):
    value: str

    type: Optional[Literal["a"]] = None
