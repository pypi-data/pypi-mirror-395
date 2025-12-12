# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["AmountOutput"]


class AmountOutput(BaseModel):
    currency_code: str
    """The currency code of the amount."""

    value: str
    """The value of the amount in the smallest unit of the currency."""
