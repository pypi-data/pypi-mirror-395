# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .nested_request_model_c_param import NestedRequestModelCParam

__all__ = ["NestedRequestModelBParam"]


class NestedRequestModelBParam(TypedDict, total=False):
    bar: NestedRequestModelCParam
