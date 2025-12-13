# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["MonitorEventResponse"]


class MonitorEventResponse(BaseModel):
    event_id: str
    """A unique monitor event ID."""

    monitor_id: str
    """Monitor ID associated with this event."""

    created_at: Optional[datetime] = None
    """The time the monitor event was created in UTC."""
