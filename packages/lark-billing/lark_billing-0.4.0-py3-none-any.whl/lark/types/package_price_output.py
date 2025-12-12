# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel
from .amount_output import AmountOutput

__all__ = ["PackagePriceOutput"]


class PackagePriceOutput(BaseModel):
    amount: AmountOutput

    package_units: int

    rounding_behavior: Literal["round_up", "round_down"]

    price_type: Optional[Literal["package"]] = None
