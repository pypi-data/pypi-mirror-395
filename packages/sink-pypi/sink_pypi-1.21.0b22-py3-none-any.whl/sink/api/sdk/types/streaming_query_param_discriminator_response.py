# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["StreamingQueryParamDiscriminatorResponse"]


class StreamingQueryParamDiscriminatorResponse(BaseModel):
    completion: str

    model: Optional[str] = None
