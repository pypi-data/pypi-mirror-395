# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "PurchaseRequestVerificationCodeResponse",
    "CodeRequest",
    "Purchase",
    "PurchaseDisplayName",
    "PurchasePrice",
    "PurchaseVerification",
]


class CodeRequest(BaseModel):
    attempt: int
    """Current attempt number"""

    max_attempts: int
    """Maximum number of attempts"""

    next_attempt_at: Optional[str] = None
    """ISO timestamp of next attempt (null if not scheduled)"""

    retry_after: Optional[int] = None
    """Seconds until next attempt (null if not scheduled)"""

    status: Literal["not_requested", "pending", "success", "failed"]
    """Current status of the code request"""


class PurchaseDisplayName(BaseModel):
    en: str
    """Name in English."""

    ru: str
    """Name in Russian."""


class PurchasePrice(BaseModel):
    amount: str
    """Monetary amount as a string with up to 2 decimal places."""

    currency_code: str
    """ISO 4217 currency code."""


class PurchaseVerification(BaseModel):
    code: str
    """Verification code for account."""

    password: str
    """Account password."""

    received_at: str
    """
    **Code Retrieval Timestamp.** Marks when verification code was successfully
    fetched from the provider (not when purchase was created).

    **Example timeline.**

    - `created_at`: `2024-11-19T10:00:00Z` (purchase created)
    - `received_at`: `2024-11-19T10:05:02Z` (code requested 5 minutes later)

    **Note.** These timestamps may be identical if code is requested immediately
    after purchase.
    """


class Purchase(BaseModel):
    id: int
    """Unique purchase identifier."""

    country_code: str
    """ISO 3166-1 alpha-2 country code."""

    created_at: str
    """Purchase creation time in ISO 8601 format (UTC)."""

    display_name: PurchaseDisplayName

    phone_number: str
    """
    **E.164 International Format.** Phone number with country code prefix (e.g.,
    `+12025550123` for US, `+79991234567` for Russia).

    **Usage.** This is your Telegram account login. Use it with `verification.code`
    and `verification.password` to access the account.
    """

    price: PurchasePrice
    """
    **Final Price After Discount.** The actual amount deducted from your balance,
    with your personal discount already applied.

    **To see pricing breakdown before purchase.** Check
    `GET /accounts/:country_code` which shows both discounted price and original
    `base_price`.

    **Discount eligibility.** Based on your total successful purchase count. Higher
    volume = bigger discounts.
    """

    status: Literal["PENDING", "SUCCESS", "ERROR", "REFUND"]
    """
    **Purchase Status Lifecycle.** `PENDING` (initial) → `SUCCESS` (after code
    request) or `ERROR` (provider failure). Any status can transition to `REFUND`
    via admin action.

    **Important.** Status is immutable once set to `SUCCESS`, `ERROR`, or `REFUND`.

    **Filter options**

    - `PENDING` - code not requested.
    - `SUCCESS` - code ready.
    - `ERROR` - provider failed.
    - `REFUND` - money returned.
    """

    verification: Optional[PurchaseVerification] = None
    """
    **Verification Credentials.** Login credentials for the purchased Telegram
    account. Initially `null` after purchase creation.

    **Availability.** Populated after calling `POST /purchases/:id/request-code`.
    Once received, credentials are permanent and cannot be re-requested.

    **Security.** Verification data is only visible to the purchase owner.
    """


class PurchaseRequestVerificationCodeResponse(BaseModel):
    code_request: CodeRequest

    purchase: Purchase
