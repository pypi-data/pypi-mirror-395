# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["PageNumberWithoutCurrentPageResponseListWithoutCurrentPageResponseParams"]


class PageNumberWithoutCurrentPageResponseListWithoutCurrentPageResponseParams(TypedDict, total=False):
    page: int

    page_size: int

    prop_to_not_mess_with_infer_for_other_pages: bool
