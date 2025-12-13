# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo
from .shared_params.shipping_address import ShippingAddress

__all__ = ["MethodConfigShouldNotShowUpInAPIDocsParams"]


class MethodConfigShouldNotShowUpInAPIDocsParams(TypedDict, total=False):
    product_id: str
    """Specifies the configuration (e.g.

    physical card art) that the card should be manufactured with, and only applies
    to cards of type `PHYSICAL` [beta]. This must be configured with Lithic before
    use.
    """

    shipping_method: Literal["STANDARD", "STANDARD_WITH_TRACKING", "EXPEDITED"]
    """Shipping method for the card.

    Use of options besides `STANDARD` require additional permissions.

    - `STANDARD` - USPS regular mail or similar international option, with no
      tracking
    - `STANDARD_WITH_TRACKING` - USPS regular mail or similar international option,
      with tracking
    - `EXPEDITED` - FedEx Standard Overnight or similar international option, with
      tracking
    """

    shipping_address: Annotated[ShippingAddress, PropertyInfo(alias="shippingAddress")]
    """If omitted, the previous shipping address will be used."""
