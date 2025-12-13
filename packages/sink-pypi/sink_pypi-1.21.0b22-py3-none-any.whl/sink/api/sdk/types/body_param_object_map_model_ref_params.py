# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .object_map_model_param import ObjectMapModelParam

__all__ = ["BodyParamObjectMapModelRefParams"]


class BodyParamObjectMapModelRefParams(TypedDict, total=False):
    model_ref: Required[ObjectMapModelParam]

    name: Required[str]
