# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["MonitorUpdateResponse"]


class MonitorUpdateResponse(BaseModel):
    modified_at: datetime
    """The time the monitor was last modified in UTC."""

    monitor_id: str
    """A unique monitor ID."""

    status: Literal["active", "inactive"]
    """Status of the monitor.

    Can be `active` or `inactive`. Inactive monitors no longer record and evaluate
    events.
    """
