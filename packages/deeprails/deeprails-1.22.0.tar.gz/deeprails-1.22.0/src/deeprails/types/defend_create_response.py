# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["DefendCreateResponse"]


class DefendCreateResponse(BaseModel):
    created_at: datetime
    """The time the workflow was created in UTC."""

    status: Literal["inactive", "active"]
    """Status of the selected workflow.

    May be `inactive` or `active`. Inactive workflows will not accept events.
    """

    workflow_id: str
    """A unique workflow ID."""
