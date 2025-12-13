# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .custom_api_status_message import CustomAPIStatusMessage

__all__ = ["APIStatus"]


class APIStatus(BaseModel):
    message: CustomAPIStatusMessage
