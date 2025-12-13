# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel

__all__ = ["DiscriminatedUnion", "Foo", "Bar"]


class Foo(BaseModel):
    foo: Optional[str] = None

    type: Optional[Literal["foo"]] = None


class Bar(BaseModel):
    bar: Optional[str] = None

    type: Optional[Literal["bar"]] = None


DiscriminatedUnion: TypeAlias = Annotated[Union[Foo, Bar], PropertyInfo(discriminator="type")]
