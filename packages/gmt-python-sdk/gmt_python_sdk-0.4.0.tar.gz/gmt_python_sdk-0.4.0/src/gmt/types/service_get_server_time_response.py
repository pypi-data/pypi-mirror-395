# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ServiceGetServerTimeResponse"]


class ServiceGetServerTimeResponse(BaseModel):
    epoch_ms: int = FieldInfo(alias="epochMs")
    """Current server time in milliseconds since Unix epoch."""

    iso: str
    """Current server time in ISO 8601 format."""

    timezone: str
    """Server timezone."""
