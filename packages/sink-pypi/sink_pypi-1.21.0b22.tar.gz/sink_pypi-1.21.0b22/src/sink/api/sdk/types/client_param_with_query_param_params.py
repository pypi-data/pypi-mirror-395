# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ClientParamWithQueryParamParams"]


class ClientParamWithQueryParamParams(TypedDict, total=False):
    client_path_or_query_param: str
    """Path/Query param that can defined on the client."""

    client_query_param: str
    """Query param that can be defined on the client."""
