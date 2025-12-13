# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["ObjectMultiplePropertiesSameRefResponse", "RequiredProp", "Bar", "Foo"]


class RequiredProp(BaseModel):
    foo: Optional[str] = None


class Bar(BaseModel):
    foo: Optional[str] = None


class Foo(BaseModel):
    foo: Optional[str] = None


class ObjectMultiplePropertiesSameRefResponse(BaseModel):
    required_prop: RequiredProp

    bar: Optional[Bar] = None

    foo: Optional[Foo] = None
