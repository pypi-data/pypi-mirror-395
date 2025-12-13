# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["StreamingNoDiscriminatorParams"]


class StreamingNoDiscriminatorParams(TypedDict, total=False):
    model: Required[str]

    prompt: Required[str]
