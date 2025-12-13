# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["DefendResponse", "Capability", "Event", "EventEvaluation", "File", "Stats"]


class Capability(BaseModel):
    capability: Optional[str] = None


class EventEvaluation(BaseModel):
    attempt: Optional[str] = None
    """The attempt number or identifier for this evaluation."""

    created_at: Optional[datetime] = None
    """The time the evaluation was created in UTC."""

    error_message: Optional[str] = None
    """Error message if the evaluation failed."""

    evaluation_result: Optional[Dict[str, object]] = None
    """The result of the evaluation."""

    evaluation_status: Optional[str] = None
    """Status of the evaluation."""

    evaluation_total_cost: Optional[float] = None
    """Total cost of the evaluation."""

    guardrail_metrics: Optional[List[str]] = None
    """An array of guardrail metrics evaluated."""

    api_model_input: Optional[Dict[str, object]] = FieldInfo(alias="model_input", default=None)
    """The model input used for the evaluation."""

    api_model_output: Optional[str] = FieldInfo(alias="model_output", default=None)
    """The model output that was evaluated."""

    modified_at: Optional[datetime] = None
    """The time the evaluation was last modified in UTC."""

    nametag: Optional[str] = None
    """An optional tag for the evaluation."""

    progress: Optional[int] = None
    """Evaluation progress (0-100)."""

    run_mode: Optional[str] = None
    """Run mode used for the evaluation."""


class Event(BaseModel):
    evaluations: Optional[List[EventEvaluation]] = None
    """An array of evaluations for this event."""

    event_id: Optional[str] = None
    """A unique workflow event ID."""

    improved_model_output: Optional[str] = None
    """Improved model output after improvement tool was applied."""

    improvement_tool_status: Optional[str] = None
    """Status of the improvement tool used to improve the event."""


class File(BaseModel):
    file_id: Optional[str] = None

    file_name: Optional[str] = None

    file_size: Optional[int] = None


class Stats(BaseModel):
    outputs_below_threshold: Optional[int] = None
    """Number of AI outputs that failed the guardrails."""

    outputs_improved: Optional[int] = None
    """Number of AI outputs that were improved."""

    outputs_processed: Optional[int] = None
    """Total number of AI outputs processed by the workflow."""


class DefendResponse(BaseModel):
    automatic_hallucination_tolerance_levels: Dict[str, Literal["low", "medium", "high"]]
    """Mapping of guardrail metric names to tolerance values.

    Values can be strings (`low`, `medium`, `high`) for automatic tolerance levels.
    """

    capabilities: List[Capability]
    """Extended AI capabilities available to the event, if any.

    Can be `web_search`, `file_search`, and/or `context_awareness`.
    """

    created_at: datetime
    """The time the workflow was created in UTC."""

    custom_hallucination_threshold_values: Dict[str, float]
    """Mapping of guardrail metric names to threshold values.

    Values can be floating point numbers (0.0-1.0) for custom thresholds.
    """

    description: str
    """
    A description for the workflow, to help you remember what that workflow means to
    your organization.
    """

    events: List[Event]
    """An array of events associated with this workflow."""

    files: List[File]
    """List of files associated with the workflow.

    If this is not empty, models can search these files when performing evaluations
    or remediations
    """

    name: str
    """
    A human-readable name for the workflow that will correspond to it's workflow ID.
    """

    status: Literal["inactive", "active"]
    """Status of the selected workflow.

    May be `inactive` or `active`. Inactive workflows will not accept events.
    """

    threshold_type: Literal["custom", "automatic"]
    """Type of thresholds used to evaluate the event."""

    updated_at: datetime
    """The most recent time the workflow was updated in UTC."""

    workflow_id: str
    """A unique workflow ID used to identify the workflow in other endpoints."""

    improvement_action: Optional[Literal["regen", "fixit", "do_nothing"]] = None
    """
    The action used to improve outputs that fail one or more guardrail metrics for
    the workflow events.
    """

    stats: Optional[Stats] = None
