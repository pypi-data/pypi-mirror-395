# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["NamePropertiesIllegalJavascriptIdentifiersResponse", "_2llegalJavascriptIdentifiers"]


class _2llegalJavascriptIdentifiers(BaseModel):
    irrelevant: Optional[float] = None


NamePropertiesIllegalJavascriptIdentifiersResponse: TypeAlias = Union[_2llegalJavascriptIdentifiers, float]
