# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["Period"]


class Period(BaseModel):
    end: datetime

    start: datetime

    inclusive_end: Optional[bool] = None

    inclusive_start: Optional[bool] = None
