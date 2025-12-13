# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .card import Card
from .._models import BaseModel

__all__ = ["CardReadyWebhookEvent"]


class CardReadyWebhookEvent(BaseModel):
    id: str

    data: Card

    type: Literal["card.ready"]

    user_id: Optional[str] = None
