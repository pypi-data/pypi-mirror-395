# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypedDict

__all__ = ["AmountInputParam"]


class AmountInputParam(TypedDict, total=False):
    currency_code: Required[str]
    """The currency code of the amount."""

    value: Required[Union[float, str]]
    """The value of the amount in the smallest unit of the currency."""
