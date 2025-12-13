# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .simple_allof import SimpleAllof
from .responses_allof_cross_object import ResponsesAllofCrossObject

__all__ = ["ResponseAllofCrossResourceResponse"]


class ResponseAllofCrossResourceResponse(SimpleAllof, ResponsesAllofCrossObject):
    baz: Optional[str] = None
