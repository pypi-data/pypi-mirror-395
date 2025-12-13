# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .nested_request_model_a_param import NestedRequestModelAParam

__all__ = ["BodyParamNestedRequestModelsParams"]


class BodyParamNestedRequestModelsParams(TypedDict, total=False):
    data: NestedRequestModelAParam
