# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SimpleObject"]


class SimpleObject(TypedDict, total=False):
    bar: Required[float]
    """This is a long multi line description

    to be sure that we

    handle it correctly in our

    various SDKs.
    """
