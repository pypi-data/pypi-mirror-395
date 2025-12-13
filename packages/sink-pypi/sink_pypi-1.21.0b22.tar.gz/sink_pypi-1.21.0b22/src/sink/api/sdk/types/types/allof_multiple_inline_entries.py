# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .allof_base_parent import AllofBaseParent

__all__ = ["AllofMultipleInlineEntries"]


class AllofMultipleInlineEntries(AllofBaseParent):
    in_first_entry: Optional[str] = None

    in_second_entry: Optional[int] = None
