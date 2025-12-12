# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .period_param import PeriodParam

__all__ = ["PricingMetricCreateSummaryParams"]


class PricingMetricCreateSummaryParams(TypedDict, total=False):
    period: Required[PeriodParam]
    """The period that the summary should be computed over."""

    subject_id: Required[str]
    """The ID or external ID of the subject that the summary should be computed for."""
