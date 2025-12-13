# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict

from ..._models import BaseModel

__all__ = ["MapUnknownItemsResponse"]


class MapUnknownItemsResponse(BaseModel):
    any_map: Dict[str, object]

    unknown_map: Dict[str, object]

    unspecified_type_object_map: Dict[str, object]
