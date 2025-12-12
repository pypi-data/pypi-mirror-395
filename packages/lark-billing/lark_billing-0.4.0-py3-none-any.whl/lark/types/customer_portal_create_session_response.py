# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from .._models import BaseModel

__all__ = ["CustomerPortalCreateSessionResponse"]


class CustomerPortalCreateSessionResponse(BaseModel):
    expires_at: datetime
    """The date and time the customer portal session expires."""

    subject_id: str
    """The ID of the subject for the customer portal session."""

    url: str
    """The URL to redirect to the customer portal session."""
