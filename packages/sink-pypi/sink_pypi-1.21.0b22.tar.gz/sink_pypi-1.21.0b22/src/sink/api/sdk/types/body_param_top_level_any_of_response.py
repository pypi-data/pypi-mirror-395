# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = ["BodyParamTopLevelAnyOfResponse", "ObjectWithRequiredEnum", "SimpleObjectWithRequiredProperty"]


class ObjectWithRequiredEnum(BaseModel):
    """This is an object with required enum values"""

    kind: Literal["VIRTUAL", "PHYSICAL"]


class SimpleObjectWithRequiredProperty(BaseModel):
    """This is an object with required properties"""

    is_foo: bool


BodyParamTopLevelAnyOfResponse: TypeAlias = Union[ObjectWithRequiredEnum, SimpleObjectWithRequiredProperty]
