# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["SubscriptionResource", "CurrentPeriod"]


class CurrentPeriod(BaseModel):
    end: datetime

    start: datetime

    inclusive_end: Optional[bool] = None

    inclusive_start: Optional[bool] = None


class SubscriptionResource(BaseModel):
    id: str
    """The ID of the subscription."""

    cancels_at_end_of_cycle: bool
    """Whether the subscription will be cancelled at the end of the current cycle."""

    current_period: Optional[CurrentPeriod] = None
    """The current period of the subscription if it is active."""

    cycles_next_at: Optional[datetime] = None
    """The date and time the next cycle of the subscription will start."""

    effective_at: datetime
    """The date and time the subscription became effective."""

    metadata: Dict[str, str]

    rate_card_id: str
    """The ID of the rate card of the subscription."""

    status: Literal["active", "cancelled", "paused"]
    """The status of the subscription."""

    subject_id: str
    """The ID of the subject that the subscription is for."""
