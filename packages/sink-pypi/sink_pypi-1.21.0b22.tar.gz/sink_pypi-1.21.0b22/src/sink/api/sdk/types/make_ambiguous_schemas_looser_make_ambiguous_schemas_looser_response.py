# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["MakeAmbiguousSchemasLooserMakeAmbiguousSchemasLooserResponse"]


class MakeAmbiguousSchemasLooserMakeAmbiguousSchemasLooserResponse(BaseModel):
    any: object

    any_json: object = FieldInfo(alias="anyJson")

    any_object: Dict[str, object] = FieldInfo(alias="anyObject")

    empty: object

    empty_additional_properties: object = FieldInfo(alias="emptyAdditionalProperties")

    empty_object: object = FieldInfo(alias="emptyObject")
