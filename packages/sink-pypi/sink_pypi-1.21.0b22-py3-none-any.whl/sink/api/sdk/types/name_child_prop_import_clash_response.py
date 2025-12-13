# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from . import balance as _balance
from .._models import BaseModel

__all__ = ["NameChildPropImportClashResponse", "Balance"]


class Balance(BaseModel):
    bar: Optional[str] = None


class NameChildPropImportClashResponse(BaseModel):
    balance: Balance

    balance_model: _balance.Balance
