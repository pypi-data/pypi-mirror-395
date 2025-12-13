# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ServiceHealthCheckResponse", "Checks"]


class Checks(BaseModel):
    database: bool
    """Database connection status."""

    redis: bool
    """Redis connection status."""


class ServiceHealthCheckResponse(BaseModel):
    now: str
    """Current server time in ISO 8601 format."""

    status: Literal["ok", "degraded"]
    """Service status."""

    uptime_seconds: int = FieldInfo(alias="uptimeSeconds")
    """API uptime in seconds."""

    checks: Optional[Checks] = None
    """Detailed information about dependencies state."""
