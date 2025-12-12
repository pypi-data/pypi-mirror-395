# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .rate_card_resource import RateCardResource

__all__ = ["RateCardListResponse"]


class RateCardListResponse(BaseModel):
    has_more: bool

    rate_cards: List[RateCardResource]
