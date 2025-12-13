# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["PurchaseCreateParams"]


class PurchaseCreateParams(TypedDict, total=False):
    country_code: Required[str]
    """ISO 3166-1 alpha-2 country code."""
