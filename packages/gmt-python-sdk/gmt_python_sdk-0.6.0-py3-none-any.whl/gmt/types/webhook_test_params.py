# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["WebhookTestParams"]


class WebhookTestParams(TypedDict, total=False):
    type: Required[Literal["success", "failed"]]
    """Webhook payload type to send: `success` or `failed`."""

    url: Required[str]
    """Webhook endpoint URL. Must be a valid URL."""
