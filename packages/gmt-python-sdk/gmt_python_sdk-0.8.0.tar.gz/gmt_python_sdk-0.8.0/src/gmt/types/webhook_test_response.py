# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["WebhookTestResponse"]


class WebhookTestResponse(BaseModel):
    success: bool
    """Whether the webhook was delivered successfully (HTTP 200)."""

    error: Optional[str] = None
    """Error message if delivery failed."""

    http_code: Optional[int] = None
    """HTTP status code returned by your endpoint."""

    response_body: Optional[str] = None
    """Response body from your endpoint (truncated to 1000 characters)."""

    response_time_ms: Optional[int] = None
    """Response time in milliseconds."""
