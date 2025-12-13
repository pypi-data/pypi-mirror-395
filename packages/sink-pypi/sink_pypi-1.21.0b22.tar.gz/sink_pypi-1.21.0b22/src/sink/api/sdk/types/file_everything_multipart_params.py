# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .._types import FileTypes

__all__ = ["FileEverythingMultipartParams"]


class FileEverythingMultipartParams(TypedDict, total=False):
    b: Required[bool]

    e: Required[Literal["a", "b", "c"]]

    f: Required[float]

    file: Required[FileTypes]

    i: Required[int]

    purpose: Required[str]

    s: Required[str]
