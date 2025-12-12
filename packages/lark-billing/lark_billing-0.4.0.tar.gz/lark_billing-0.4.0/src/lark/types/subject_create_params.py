# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

__all__ = ["SubjectCreateParams"]


class SubjectCreateParams(TypedDict, total=False):
    email: Optional[str]
    """The email of the subject. Must be a valid email address."""

    external_id: Optional[str]
    """The ID of the subject in your system.

    If provided, you may use pass it to the API in place of the subject ID. Must be
    unique.
    """

    metadata: Dict[str, str]
    """Additional metadata about the subject.

    You may use this to store any custom data about the subject.
    """

    name: Optional[str]
    """The name of the subject. Used for display in the dashboard."""
