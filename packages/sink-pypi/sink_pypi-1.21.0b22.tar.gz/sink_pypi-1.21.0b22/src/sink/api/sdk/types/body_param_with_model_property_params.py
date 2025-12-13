# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .my_model_param import MyModelParam

__all__ = ["BodyParamWithModelPropertyParams"]


class BodyParamWithModelPropertyParams(TypedDict, total=False):
    foo: str

    my_model: MyModelParam
