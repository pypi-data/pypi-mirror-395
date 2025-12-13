# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ParamTimeoutParamParams"]


class ParamTimeoutParamParams(TypedDict, total=False):
    url_timeout: Annotated[float, PropertyInfo(alias="timeout")]
    """my timeout request parameter"""
