# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["SubscriptionListParams"]


class SubscriptionListParams(TypedDict, total=False):
    limit: int

    offset: int

    rate_card_id: Optional[str]
    """The ID of the rate card to list subscriptions for.

    Cannot be used with subject_id.
    """

    subject_id: Optional[str]
    """The ID or external ID of the subject to list subscriptions for.

    Cannot be used with rate_card_id.
    """
