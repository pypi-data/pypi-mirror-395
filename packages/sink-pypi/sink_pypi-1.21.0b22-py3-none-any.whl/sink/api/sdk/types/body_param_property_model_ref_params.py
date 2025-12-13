# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .my_model_param import MyModelParam

__all__ = ["BodyParamPropertyModelRefParams"]


class BodyParamPropertyModelRefParams(TypedDict, total=False):
    model_ref: Required[MyModelParam]

    name: Required[str]
