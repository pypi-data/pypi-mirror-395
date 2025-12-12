# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .checkout_callback_param import CheckoutCallbackParam

__all__ = ["SubscriptionChangeRateCardParams"]


class SubscriptionChangeRateCardParams(TypedDict, total=False):
    checkout_callback_urls: Required[CheckoutCallbackParam]
    """
    The URLs to redirect to after the checkout is completed or cancelled, if a
    checkout is required.
    """

    rate_card_id: Required[str]
    """The ID of the rate card to change the subscription to."""

    upgrade_behavior: Literal["prorate", "rate_difference"]
    """The behavior to use when upgrading the subscription.

    If 'prorate', the customer will be charged for the prorated difference. If
    'rate_difference', the customer will be charged for the difference in the rate
    cards without respect to time.
    """
