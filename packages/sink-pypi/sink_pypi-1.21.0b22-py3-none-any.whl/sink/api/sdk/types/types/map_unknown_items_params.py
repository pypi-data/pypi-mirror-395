# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["MapUnknownItemsParams"]


class MapUnknownItemsParams(TypedDict, total=False):
    any_map: Required[Dict[str, object]]

    unknown_map: Required[Dict[str, object]]

    unspecified_type_object_map: Required[Dict[str, object]]
