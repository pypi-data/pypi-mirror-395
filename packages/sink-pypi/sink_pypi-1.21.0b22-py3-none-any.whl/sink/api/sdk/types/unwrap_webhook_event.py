# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import TypeAlias

from .card_ready_webhook_event import CardReadyWebhookEvent
from .card_created_webhook_event import CardCreatedWebhookEvent
from .card_deleted_webhook_event import CardDeletedWebhookEvent
from .card_errored_webhook_event import CardErroredWebhookEvent
from .card_updated_webhook_event import CardUpdatedWebhookEvent

__all__ = ["UnwrapWebhookEvent"]

UnwrapWebhookEvent: TypeAlias = Union[
    CardCreatedWebhookEvent,
    CardReadyWebhookEvent,
    CardErroredWebhookEvent,
    CardUpdatedWebhookEvent,
    CardDeletedWebhookEvent,
]
