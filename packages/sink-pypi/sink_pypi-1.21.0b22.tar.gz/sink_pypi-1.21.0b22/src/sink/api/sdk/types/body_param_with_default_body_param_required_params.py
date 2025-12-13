# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["BodyParamWithDefaultBodyParamRequiredParams"]


class BodyParamWithDefaultBodyParamRequiredParams(TypedDict, total=False):
    my_version_body_param: str

    normal_param: Required[bool]
