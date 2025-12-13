# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Annotated, TypedDict

from .._types import Base64FileInput
from .._utils import PropertyInfo

__all__ = ["CardProvisionFooParams"]


class CardProvisionFooParams(TypedDict, total=False):
    account_token: str
    """Only required for multi-account users.

    Token identifying the account the card will be associated with. Only applicable
    if using account holder enrollment. See
    [Managing Your Program](https://docs.lithic.com/docs/managing-your-program) for
    more information.
    """

    certificate: Annotated[Union[str, Base64FileInput], PropertyInfo(format="base64")]
    """Required for `APPLE_PAY`.

    Apple's public leaf certificate. Base64 encoded in PEM format with headers
    `(-----BEGIN CERTIFICATE-----)` and trailers omitted. Provided by the device's
    wallet.
    """

    digital_wallet: Literal["APPLE_PAY", "GOOGLE_PAY", "SAMSUNG_PAY"]
    """Name of digital wallet provider."""

    nonce: Annotated[Union[str, Base64FileInput], PropertyInfo(format="base64")]
    """Required for `APPLE_PAY`.

    Base64 cryptographic nonce provided by the device's wallet.
    """

    nonce_signature: Annotated[Union[str, Base64FileInput], PropertyInfo(format="base64")]
    """Required for `APPLE_PAY`.

    Base64 cryptographic nonce provided by the device's wallet.
    """
