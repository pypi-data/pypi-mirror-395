# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .amount_output import AmountOutput

__all__ = ["InvoiceListResponse", "Invoice", "InvoiceLineItem"]


class InvoiceLineItem(BaseModel):
    amount: AmountOutput

    description: str

    price_in_unit_amount: AmountOutput

    quantity: int


class Invoice(BaseModel):
    id: str
    """The ID of the invoice."""

    created_at: datetime
    """The date and time the invoice was created."""

    hosted_url: Optional[str] = None
    """The URL of the hosted invoice."""

    line_items: List[InvoiceLineItem]
    """The line items of the invoice."""

    status: Literal["draft", "open", "paid", "uncollectible", "void"]
    """The status of the invoice."""

    subject_id: str
    """The ID of the subject for the invoice."""

    total_amount: AmountOutput
    """The total amount of the invoice."""


class InvoiceListResponse(BaseModel):
    has_more: bool

    invoices: List[Invoice]
