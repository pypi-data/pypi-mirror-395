# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .unknown_object_model_param import UnknownObjectModelParam

__all__ = ["BodyParamUnknownObjectParams"]


class BodyParamUnknownObjectParams(TypedDict, total=False):
    name: Required[str]

    unknown_object_prop: Required[UnknownObjectModelParam]
