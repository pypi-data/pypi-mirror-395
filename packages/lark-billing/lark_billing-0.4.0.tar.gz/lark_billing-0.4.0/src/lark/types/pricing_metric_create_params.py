# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr

__all__ = [
    "PricingMetricCreateParams",
    "Aggregation",
    "AggregationSumAggregationPricingMetricInterface",
    "AggregationCountAggregationPricingMetricInterface",
    "AggregationMaxAggregationPricingMetricInterface",
    "AggregationLastAggregationPricingMetricInterface",
    "AggregationCustomAggregationPricingMetricInterface",
]


class PricingMetricCreateParams(TypedDict, total=False):
    aggregation: Required[Aggregation]
    """The aggregation function used to compute the value of the pricing metric."""

    event_name: Required[str]
    """The name of the event that the pricing metric is computed on."""

    name: Required[str]
    """The name of the pricing metric."""

    unit: Required[str]
    """Unit of measurement for the pricing metric."""

    dimensions: Optional[SequenceNotStr[str]]
    """The dimensions by which the events are grouped to compute the pricing metric."""


class AggregationSumAggregationPricingMetricInterface(TypedDict, total=False):
    aggregation_type: Required[Literal["sum"]]

    value_field: Required[str]
    """Field to sum over."""


class AggregationCountAggregationPricingMetricInterface(TypedDict, total=False):
    aggregation_type: Required[Literal["count"]]


class AggregationMaxAggregationPricingMetricInterface(TypedDict, total=False):
    aggregation_type: Required[Literal["max"]]

    value_field: Required[str]
    """Field to get the max value of."""


class AggregationLastAggregationPricingMetricInterface(TypedDict, total=False):
    aggregation_type: Required[Literal["last"]]

    value_field: Required[str]
    """Field to get the last value of."""


class AggregationCustomAggregationPricingMetricInterface(TypedDict, total=False):
    aggregation_type: Required[Literal["custom"]]

    custom_expression: Required[str]
    """Custom expression to compute the pricing metric.

    Please email team@uselark.ai to enable this feature.
    """


Aggregation: TypeAlias = Union[
    AggregationSumAggregationPricingMetricInterface,
    AggregationCountAggregationPricingMetricInterface,
    AggregationMaxAggregationPricingMetricInterface,
    AggregationLastAggregationPricingMetricInterface,
    AggregationCustomAggregationPricingMetricInterface,
]
