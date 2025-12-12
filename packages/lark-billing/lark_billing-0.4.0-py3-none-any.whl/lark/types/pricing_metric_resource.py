# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "PricingMetricResource",
    "Aggregation",
    "AggregationSumAggregationPricingMetricResource",
    "AggregationCountAggregationPricingMetricResource",
    "AggregationMaxAggregationPricingMetricResource",
    "AggregationLastAggregationPricingMetricResource",
]


class AggregationSumAggregationPricingMetricResource(BaseModel):
    aggregation_type: Literal["sum"]

    value_field: str
    """The field to sum over."""


class AggregationCountAggregationPricingMetricResource(BaseModel):
    aggregation_type: Literal["count"]


class AggregationMaxAggregationPricingMetricResource(BaseModel):
    aggregation_type: Literal["max"]

    value_field: str
    """The field to get the max value of."""


class AggregationLastAggregationPricingMetricResource(BaseModel):
    aggregation_type: Literal["last"]

    value_field: str
    """The field to get the last value of."""


Aggregation: TypeAlias = Annotated[
    Union[
        AggregationSumAggregationPricingMetricResource,
        AggregationCountAggregationPricingMetricResource,
        AggregationMaxAggregationPricingMetricResource,
        AggregationLastAggregationPricingMetricResource,
    ],
    PropertyInfo(discriminator="aggregation_type"),
]


class PricingMetricResource(BaseModel):
    id: str
    """The ID of the pricing metric."""

    aggregation: Aggregation
    """The aggregation function used to compute the value of the pricing metric."""

    event_name: str
    """The event name that the pricing metric is computed on."""

    name: str
    """The name of the pricing metric."""

    unit: str
    """The unit of the value computed by the pricing metric."""

    dimensions: Optional[List[str]] = None
    """The dimensions by which the events are grouped to compute the pricing metric."""
