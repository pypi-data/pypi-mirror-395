# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["ObjectMultipleArrayPropertiesSameRefResponse", "RequiredProp", "Bar", "Foo"]


class RequiredProp(BaseModel):
    foo: Optional[str] = None


class Bar(BaseModel):
    foo: Optional[str] = None


class Foo(BaseModel):
    foo: Optional[str] = None


class ObjectMultipleArrayPropertiesSameRefResponse(BaseModel):
    required_prop: List[RequiredProp]

    bar: Optional[List[Bar]] = None

    foo: Optional[List[Foo]] = None
