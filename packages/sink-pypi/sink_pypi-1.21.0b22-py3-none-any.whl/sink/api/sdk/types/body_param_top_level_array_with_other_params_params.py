# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from .shared_params.basic_shared_model_object import BasicSharedModelObject

__all__ = ["BodyParamTopLevelArrayWithOtherParamsParams"]


class BodyParamTopLevelArrayWithOtherParamsParams(TypedDict, total=False):
    id: Required[str]

    items: Required[Iterable[BasicSharedModelObject]]
