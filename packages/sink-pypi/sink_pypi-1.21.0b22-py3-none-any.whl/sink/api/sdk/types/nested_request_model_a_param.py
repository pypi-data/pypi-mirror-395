# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .nested_request_model_b_param import NestedRequestModelBParam

__all__ = ["NestedRequestModelAParam"]


class NestedRequestModelAParam(TypedDict, total=False):
    foo: NestedRequestModelBParam
