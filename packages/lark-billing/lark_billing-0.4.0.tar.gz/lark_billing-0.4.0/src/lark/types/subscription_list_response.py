# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .subscription_resource import SubscriptionResource

__all__ = ["SubscriptionListResponse"]


class SubscriptionListResponse(BaseModel):
    has_more: bool

    subscriptions: List[SubscriptionResource]
