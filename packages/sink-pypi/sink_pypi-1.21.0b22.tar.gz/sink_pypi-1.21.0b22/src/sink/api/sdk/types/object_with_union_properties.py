# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import TypeAlias

from .._models import BaseModel
from .my_model import MyModel
from .shared.simple_object import SimpleObject

__all__ = ["ObjectWithUnionProperties", "Bar", "BarObjectWithModelProperty"]


class BarObjectWithModelProperty(BaseModel):
    foo: Optional[str] = None

    my_model: Optional[MyModel] = None


Bar: TypeAlias = Union[SimpleObject, BarObjectWithModelProperty]


class ObjectWithUnionProperties(BaseModel):
    bar: Bar

    foo: Union[float, str, bool, object]
