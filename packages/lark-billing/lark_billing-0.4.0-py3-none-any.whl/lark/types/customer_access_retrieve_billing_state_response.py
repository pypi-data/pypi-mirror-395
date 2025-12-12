# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["CustomerAccessRetrieveBillingStateResponse", "ActiveSubscription", "UsageData"]


class ActiveSubscription(BaseModel):
    rate_card_id: str

    subscription_id: str


class UsageData(BaseModel):
    included_units: int

    pricing_metric_id: str

    rate_name: str

    used_units: str


class CustomerAccessRetrieveBillingStateResponse(BaseModel):
    active_subscriptions: List[ActiveSubscription]
    """List of active subscriptions the subject is subscribed to."""

    has_active_subscription: bool
    """Whether the subject has an active subscription."""

    has_overage_for_usage: bool
    """
    Whether the subject has exceeded the included usage (if any) on a usage-based
    rate they are subscribed to.
    """

    usage_data: List[UsageData]
    """The usage data for the usage-based rates the subject is subscribed to."""
