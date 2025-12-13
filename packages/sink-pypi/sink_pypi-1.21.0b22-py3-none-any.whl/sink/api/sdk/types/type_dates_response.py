# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import date

from .._models import BaseModel

__all__ = ["TypeDatesResponse"]


class TypeDatesResponse(BaseModel):
    required_date: date

    required_nullable_date: Optional[date] = None

    list_date: Optional[List[date]] = None

    oneof_date: Union[date, int, None] = None

    optional_date: Optional[date] = None
