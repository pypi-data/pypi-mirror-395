# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ClientCreateParams"]


class ClientCreateParams(TypedDict, total=False):
    account_token: Required[str]

    name: Required[str]
