# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .model_string import ModelString

__all__ = ["PrimitiveStringsParams"]


class PrimitiveStringsParams(TypedDict, total=False):
    string_param: ModelString
