# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, Annotated, TypedDict

from .._types import Base64FileInput
from .._utils import PropertyInfo

__all__ = ["FileCreateBase64Params"]


class FileCreateBase64Params(TypedDict, total=False):
    file: Required[Annotated[Union[str, Base64FileInput], PropertyInfo(format="base64")]]

    purpose: Required[str]
