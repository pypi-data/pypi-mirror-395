# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .amount_input_param import AmountInputParam

__all__ = ["PackagePriceInputParam"]


class PackagePriceInputParam(TypedDict, total=False):
    amount: Required[AmountInputParam]

    package_units: Required[int]

    rounding_behavior: Required[Literal["round_up", "round_down"]]

    price_type: Literal["package"]
