# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, TypedDict

from .checkout_callback_param import CheckoutCallbackParam

__all__ = ["SubscriptionCreateParams"]


class SubscriptionCreateParams(TypedDict, total=False):
    checkout_callback_urls: Required[CheckoutCallbackParam]
    """
    The URLs to redirect to after the checkout is completed or cancelled, if a
    checkout is required.
    """

    rate_card_id: Required[str]
    """The ID of the rate card to use for the subscription."""

    subject_id: Required[str]
    """The ID or external ID of the subject to create the subscription for."""

    create_checkout_session: Literal["when_required", "always"]
    """
    Determines whether a checkout session is always required even if the subject has
    a payment method on file. By default, if the subject has a payment method on
    file or the subscription is for a free plan, the subscription will be created
    and billed for immediately (if for a paid plan).
    """

    metadata: Dict[str, str]
    """Additional metadata about the subscription.

    You may use this to store any custom data about the subscription.
    """
