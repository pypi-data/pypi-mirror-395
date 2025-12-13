# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["WorkflowEventResponse"]


class WorkflowEventResponse(BaseModel):
    created_at: datetime
    """The time the event was created in UTC."""

    event_id: str
    """A unique workflow event ID."""

    status: Literal["In Progress", "Completed"]
    """Status of the event."""

    workflow_id: str
    """Workflow ID associated with the event."""
