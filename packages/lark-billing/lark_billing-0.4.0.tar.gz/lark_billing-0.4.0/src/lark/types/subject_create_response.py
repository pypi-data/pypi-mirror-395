# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["SubjectCreateResponse"]


class SubjectCreateResponse(BaseModel):
    id: str
    """The ID of the subject."""

    created_at: datetime
    """The date and time the subject was created."""

    email: Optional[str] = None
    """The email of the subject."""

    external_id: Optional[str] = None
    """The ID of the subject in your system.

    You may pass it to the API in place of the subject ID.
    """

    metadata: Dict[str, str]
    """Additional metadata about the subject.

    You may use this to store any custom data about the subject.
    """

    name: Optional[str] = None
    """The name of the subject. Used for display in the dashboard."""
