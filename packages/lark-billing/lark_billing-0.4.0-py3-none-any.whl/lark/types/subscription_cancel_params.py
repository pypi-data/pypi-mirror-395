# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

__all__ = ["SubscriptionCancelParams"]


class SubscriptionCancelParams(TypedDict, total=False):
    cancel_at_end_of_cycle: Literal[True]
    """Whether to cancel the subscription at end of cycle."""

    reason: Optional[str]
    """The reason for cancelling the subscription."""
