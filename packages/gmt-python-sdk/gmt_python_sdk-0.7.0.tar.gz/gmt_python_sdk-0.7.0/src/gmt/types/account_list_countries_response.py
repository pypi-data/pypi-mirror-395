# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["AccountListCountriesResponse", "DisplayName", "Price"]


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


class AccountListCountriesResponse(BaseModel):
    available: bool
    """Whether the country is available for purchase."""

    country_code: str
    """Country code (ISO 3166-1 alpha-2)."""

    display_name: DisplayName

    price: Price
