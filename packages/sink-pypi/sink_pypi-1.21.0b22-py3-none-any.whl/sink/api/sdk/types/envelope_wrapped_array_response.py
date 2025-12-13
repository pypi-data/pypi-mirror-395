# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .shared.object_with_child_ref import ObjectWithChildRef

__all__ = ["EnvelopeWrappedArrayResponse"]

EnvelopeWrappedArrayResponse: TypeAlias = List[ObjectWithChildRef]
