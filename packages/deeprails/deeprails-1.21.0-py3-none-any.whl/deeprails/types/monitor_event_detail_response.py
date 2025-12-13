# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["MonitorEventDetailResponse", "Capability", "File"]


class Capability(BaseModel):
    capability: Optional[str] = None
    """The type of capability."""


class File(BaseModel):
    file_id: Optional[str] = None
    """The ID of the file."""

    file_name: Optional[str] = None
    """The name of the file."""

    file_size: Optional[int] = None
    """The size of the file in bytes."""


class MonitorEventDetailResponse(BaseModel):
    capabilities: Optional[List[Capability]] = None
    """The capabilities associated with the monitor event."""

    eval_time: Optional[str] = None
    """The time spent on the evaluation in seconds."""

    evaluation_result: Optional[Dict[str, object]] = None
    """The result of the evaluation of the monitor event."""

    event_id: Optional[str] = None
    """A unique monitor event ID."""

    files: Optional[List[File]] = None
    """The files associated with the monitor event."""

    guardrail_metrics: Optional[List[str]] = None
    """The guardrail metrics evaluated by the monitor event."""

    api_model_input: Optional[Dict[str, object]] = FieldInfo(alias="model_input", default=None)
    """The model input used to create the monitor event."""

    api_model_output: Optional[str] = FieldInfo(alias="model_output", default=None)
    """The output evaluated by the monitor event."""

    monitor_id: Optional[str] = None
    """Monitor ID associated with this event."""

    nametag: Optional[str] = None
    """A human-readable tag for the monitor event."""

    run_mode: Optional[Literal["precision_plus", "precision", "smart", "economy"]] = None
    """The run mode used to evaluate the monitor event."""

    status: Optional[Literal["in_progress", "completed", "canceled", "queued", "failed"]] = None
    """Status of the monitor event's evaluation."""

    timestamp: Optional[datetime] = None
    """The time the monitor event was created in UTC."""
