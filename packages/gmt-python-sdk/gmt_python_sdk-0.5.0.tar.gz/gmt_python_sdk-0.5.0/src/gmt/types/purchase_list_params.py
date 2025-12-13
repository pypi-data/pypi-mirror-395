# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["PurchaseListParams"]


class PurchaseListParams(TypedDict, total=False):
    page: Required[int]
    """Page number (starts from 1)."""

    page_size: Required[int]
    """Number of items per page (max 50)."""

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
