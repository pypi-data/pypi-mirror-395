# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["ModelWithEscapedName", "InlineObject"]


class InlineObject(BaseModel):
    foo: Optional[float] = None


class ModelWithEscapedName(BaseModel):
    inline_object: InlineObject

    name: str
