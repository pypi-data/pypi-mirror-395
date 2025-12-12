# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .flat_price_input_param import FlatPriceInputParam
from .package_price_input_param import PackagePriceInputParam

__all__ = [
    "RateCardCreateParams",
    "FixedRate",
    "FixedRatePrice",
    "UsageBasedRate",
    "UsageBasedRateCreateSimpleUsageBasedRateRequest",
    "UsageBasedRateCreateSimpleUsageBasedRateRequestPrice",
    "UsageBasedRateCreateDimensionalUsageBasedRateRequest",
    "UsageBasedRateCreateDimensionalUsageBasedRateRequestDimension",
    "UsageBasedRateCreateDimensionalUsageBasedRateRequestPricingMatrix",
    "UsageBasedRateCreateDimensionalUsageBasedRateRequestPricingMatrixCell",
    "UsageBasedRateCreateDimensionalUsageBasedRateRequestPricingMatrixCellPrice",
]


class RateCardCreateParams(TypedDict, total=False):
    billing_interval: Required[Literal["monthly", "yearly"]]
    """How often the customer will be billed for this rate card."""

    name: Required[str]
    """The name of the rate card displayed to the customer."""

    description: Optional[str]
    """The description of the rate card displayed to the customer."""

    fixed_rates: Iterable[FixedRate]
    """The fixed rates of the rate card.

    These are billed at the start of each billing cycle.
    """

    metadata: Dict[str, str]

    usage_based_rates: Iterable[UsageBasedRate]
    """The usage based rates of the rate card.

    These are billed at the end of each billing cycle.
    """


FixedRatePrice: TypeAlias = Union[FlatPriceInputParam, PackagePriceInputParam]


class FixedRate(TypedDict, total=False):
    name: Required[str]
    """The name of the rate displayed to the customer."""

    price: Required[FixedRatePrice]
    """Flat price is a price that linearly scales with the quantity."""

    description: Optional[str]
    """The description of the rate displayed to the customer."""


UsageBasedRateCreateSimpleUsageBasedRateRequestPrice: TypeAlias = Union[FlatPriceInputParam, PackagePriceInputParam]


class UsageBasedRateCreateSimpleUsageBasedRateRequest(TypedDict, total=False):
    name: Required[str]
    """The name of the rate displayed to the customer."""

    price: Required[UsageBasedRateCreateSimpleUsageBasedRateRequestPrice]
    """Flat price is a price that linearly scales with the quantity."""

    pricing_metric_id: Required[str]
    """The ID of the pricing metric to use for this rate."""

    usage_based_rate_type: Required[Literal["simple"]]

    description: Optional[str]
    """The description of the rate displayed to the customer."""

    included_units: int
    """The number of units included in the rate before the price is applied."""


class UsageBasedRateCreateDimensionalUsageBasedRateRequestDimension(TypedDict, total=False):
    key: Required[str]
    """The name of the dimension.

    This is used to identify the dimension in the pricing matrix.
    """

    values: Required[SequenceNotStr[str]]
    """A list of possible values for the dimension."""

    description: Optional[str]
    """The description of the dimension."""


UsageBasedRateCreateDimensionalUsageBasedRateRequestPricingMatrixCellPrice: TypeAlias = Union[
    FlatPriceInputParam, PackagePriceInputParam
]


class UsageBasedRateCreateDimensionalUsageBasedRateRequestPricingMatrixCell(TypedDict, total=False):
    dimension_coordinates: Required[Dict[str, str]]
    """
    A key-value mapping of dimension keys and values to identify the price for a
    given set of dimension values.
    """

    price: Required[UsageBasedRateCreateDimensionalUsageBasedRateRequestPricingMatrixCellPrice]
    """The price for the cell."""


class UsageBasedRateCreateDimensionalUsageBasedRateRequestPricingMatrix(TypedDict, total=False):
    cells: Required[Iterable[UsageBasedRateCreateDimensionalUsageBasedRateRequestPricingMatrixCell]]


class UsageBasedRateCreateDimensionalUsageBasedRateRequest(TypedDict, total=False):
    dimensions: Required[Iterable[UsageBasedRateCreateDimensionalUsageBasedRateRequestDimension]]
    """The dimensions of the rate."""

    name: Required[str]
    """The name of the rate displayed to the customer."""

    pricing_matrix: Required[UsageBasedRateCreateDimensionalUsageBasedRateRequestPricingMatrix]
    """The pricing matrix of the rate."""

    pricing_metric_id: Required[str]
    """The ID of the pricing metric to use for this rate."""

    usage_based_rate_type: Required[Literal["dimensional"]]

    description: Optional[str]
    """The description of the rate displayed to the customer."""

    included_units: int
    """The number of units included in the rate before the price is applied."""


UsageBasedRate: TypeAlias = Union[
    UsageBasedRateCreateSimpleUsageBasedRateRequest, UsageBasedRateCreateDimensionalUsageBasedRateRequest
]
