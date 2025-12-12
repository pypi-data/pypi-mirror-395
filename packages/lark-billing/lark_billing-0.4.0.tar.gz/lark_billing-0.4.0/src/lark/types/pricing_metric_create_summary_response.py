# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .period import Period
from .._models import BaseModel

__all__ = ["PricingMetricCreateSummaryResponse"]


class PricingMetricCreateSummaryResponse(BaseModel):
    id: str
    """The ID of the pricing metric summary."""

    period: Period
    """The period that the summary is computed over."""

    pricing_metric_id: str
    """The ID of the pricing metric that the summary is for."""

    subject_id: str
    """The ID of the subject that the summary is for."""

    value: Optional[str] = None
    """The computed value of the pricing metric for the period.

    If the pricing metric does not have any usage events for the period, this will
    be `null`.
    """
