# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .pricing_metric_resource import PricingMetricResource

__all__ = ["PricingMetricListResponse"]


class PricingMetricListResponse(BaseModel):
    has_more: bool

    pricing_metrics: List[PricingMetricResource]
