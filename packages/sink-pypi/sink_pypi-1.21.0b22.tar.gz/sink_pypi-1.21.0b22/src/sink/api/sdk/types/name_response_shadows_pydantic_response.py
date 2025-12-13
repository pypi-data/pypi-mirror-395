# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import typing_extensions
from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["NameResponseShadowsPydanticResponse"]


class NameResponseShadowsPydanticResponse(BaseModel):
    parse_raw_: str = FieldInfo(alias="parse_raw")

    resource_id: Optional[str] = FieldInfo(alias="model_id", default=None)

    @property
    @typing_extensions.deprecated("The resource_id property should be used instead")
    def model_id(self) -> Optional[str]:
        return self.resource_id
