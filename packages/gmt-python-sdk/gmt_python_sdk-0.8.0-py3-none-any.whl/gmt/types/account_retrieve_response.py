# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["AccountRetrieveResponse", "Discount", "DisplayName", "Price"]


class Discount(BaseModel):
    base_price: str
    """Original price without discount."""

    percent: float
    """Discount percentage applied to this user."""


class DisplayName(BaseModel):
    en: str
    """Name in English."""

    ru: str
    """Name in Russian."""


class Price(BaseModel):
    amount: str
    """Monetary amount as a string with up to 2 decimal places."""

    currency_code: str
    """ISO 4217 currency code."""


class AccountRetrieveResponse(BaseModel):
    available: bool
    """Indicates if account is available for purchase."""

    country_code: str
    """ISO 3166-1 alpha-2 country code (e.g., US, RU, GB)."""

    discount: Discount

    display_name: DisplayName

    price: Price

    tags: List[Literal["HIGH_QUALITY", "HIGH_DEMAND"]]
    """Account tags (e.g., HIGH_QUALITY for premium accounts)."""
