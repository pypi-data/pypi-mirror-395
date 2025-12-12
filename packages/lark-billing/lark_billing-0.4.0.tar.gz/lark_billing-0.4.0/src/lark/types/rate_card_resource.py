# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .flat_price_output import FlatPriceOutput
from .package_price_output import PackagePriceOutput

__all__ = [
    "RateCardResource",
    "FixedRate",
    "FixedRatePrice",
    "UsageBasedRate",
    "UsageBasedRateSimpleUsageBasedRateInterface",
    "UsageBasedRateSimpleUsageBasedRateInterfacePrice",
    "UsageBasedRateDimensionalUsageBasedRateInterface",
    "UsageBasedRateDimensionalUsageBasedRateInterfaceDimension",
    "UsageBasedRateDimensionalUsageBasedRateInterfacePricingMatrix",
    "UsageBasedRateDimensionalUsageBasedRateInterfacePricingMatrixCell",
    "UsageBasedRateDimensionalUsageBasedRateInterfacePricingMatrixCellPrice",
]

FixedRatePrice: TypeAlias = Annotated[
    Union[FlatPriceOutput, PackagePriceOutput], PropertyInfo(discriminator="price_type")
]


class FixedRate(BaseModel):
    id: str

    description: Optional[str] = None

    name: str

    price: FixedRatePrice
    """Flat price is a price that linearly scales with the quantity."""


UsageBasedRateSimpleUsageBasedRateInterfacePrice: TypeAlias = Annotated[
    Union[FlatPriceOutput, PackagePriceOutput], PropertyInfo(discriminator="price_type")
]


class UsageBasedRateSimpleUsageBasedRateInterface(BaseModel):
    id: str

    description: Optional[str] = None

    included_units: int

    name: str

    price: UsageBasedRateSimpleUsageBasedRateInterfacePrice
    """Flat price is a price that linearly scales with the quantity."""

    pricing_metric_id: str

    usage_based_rate_type: Optional[Literal["simple"]] = None


class UsageBasedRateDimensionalUsageBasedRateInterfaceDimension(BaseModel):
    description: Optional[str] = None

    key: str

    values: List[str]


UsageBasedRateDimensionalUsageBasedRateInterfacePricingMatrixCellPrice: TypeAlias = Annotated[
    Union[FlatPriceOutput, PackagePriceOutput], PropertyInfo(discriminator="price_type")
]


class UsageBasedRateDimensionalUsageBasedRateInterfacePricingMatrixCell(BaseModel):
    dimension_coordinates: Dict[str, str]

    price: UsageBasedRateDimensionalUsageBasedRateInterfacePricingMatrixCellPrice
    """Flat price is a price that linearly scales with the quantity."""


class UsageBasedRateDimensionalUsageBasedRateInterfacePricingMatrix(BaseModel):
    cells: List[UsageBasedRateDimensionalUsageBasedRateInterfacePricingMatrixCell]


class UsageBasedRateDimensionalUsageBasedRateInterface(BaseModel):
    id: str

    description: Optional[str] = None

    dimensions: List[UsageBasedRateDimensionalUsageBasedRateInterfaceDimension]

    included_units: int

    name: str

    pricing_matrix: UsageBasedRateDimensionalUsageBasedRateInterfacePricingMatrix

    pricing_metric_id: str

    usage_based_rate_type: Optional[Literal["dimensional"]] = None


UsageBasedRate: TypeAlias = Annotated[
    Union[UsageBasedRateSimpleUsageBasedRateInterface, UsageBasedRateDimensionalUsageBasedRateInterface],
    PropertyInfo(discriminator="usage_based_rate_type"),
]


class RateCardResource(BaseModel):
    id: str
    """The ID of the rate card."""

    billing_interval: Literal["monthly", "yearly"]
    """How often the customer will be billed for this rate card."""

    created_at: datetime
    """The date and time the rate card was created."""

    fixed_rates: List[FixedRate]
    """The fixed rates of the rate card."""

    metadata: Dict[str, str]
    """Additional metadata about the rate card.

    You may use this to store any custom data about the rate card.
    """

    name: str
    """The name of the rate card."""

    updated_at: datetime
    """The date and time the rate card was last updated."""

    usage_based_rates: List[UsageBasedRate]
    """The usage based rates of the rate card."""

    description: Optional[str] = None
    """The description of the rate card."""
