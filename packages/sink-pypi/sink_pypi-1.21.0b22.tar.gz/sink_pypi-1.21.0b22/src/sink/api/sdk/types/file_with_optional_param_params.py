# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .._types import FileTypes

__all__ = ["FileWithOptionalParamParams"]


class FileWithOptionalParamParams(TypedDict, total=False):
    image: Required[FileTypes]
    """The image to edit.

    Must be a valid PNG file, less than 4MB, and square. If mask is not provided,
    image must have transparency, which will be used as the mask.
    """

    prompt: Required[str]
    """A text description of the desired image(s).

    The maximum length is 1000 characters.
    """

    mask: FileTypes
    """An additional image whose fully transparent areas (e.g.

    where alpha is zero) indicate where `image` should be edited. Must be a valid
    PNG file, less than 4MB, and have the same dimensions as `image`.
    """
