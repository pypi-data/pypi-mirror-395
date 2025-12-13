# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["PurchaseRequestVerificationCodeParams"]


class PurchaseRequestVerificationCodeParams(TypedDict, total=False):
    callback_url: str
    """URL to receive webhook notification when code is received.

    POST request will be sent with either `WebhookSuccessPayload` or
    `WebhookFailedPayload`.

    **Retry policy.** If your endpoint does not return HTTP 200, webhook will be
    retried up to 3 times with delays: immediately, after 10 seconds, after 30
    seconds. Any non-200 response triggers retry.
    """
