# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["WorkflowEventDetailResponse", "EvaluationHistory", "Capability", "File"]


class EvaluationHistory(BaseModel):
    attempt: Optional[str] = None

    created_at: Optional[datetime] = None

    error_message: Optional[str] = None

    evaluation_result: Optional[Dict[str, object]] = None

    evaluation_status: Optional[str] = None

    evaluation_total_cost: Optional[float] = None

    guardrail_metrics: Optional[List[str]] = None

    api_model_input: Optional[Dict[str, object]] = FieldInfo(alias="model_input", default=None)

    api_model_output: Optional[str] = FieldInfo(alias="model_output", default=None)

    modified_at: Optional[datetime] = None

    nametag: Optional[str] = None

    progress: Optional[int] = None

    run_mode: Optional[str] = None


class Capability(BaseModel):
    capability: Optional[str] = None


class File(BaseModel):
    file_id: Optional[str] = None

    file_name: Optional[str] = None

    file_size: Optional[int] = None


class WorkflowEventDetailResponse(BaseModel):
    evaluation_history: List[EvaluationHistory]
    """History of evaluations for the event."""

    evaluation_result: Dict[str, object]
    """
    Evaluation result consisting of average scores and rationales for each of the
    evaluated guardrail metrics.
    """

    event_id: str
    """A unique workflow event ID."""

    filtered: bool
    """Whether the event was filtered and requires improvement."""

    improved_model_output: str
    """
    Improved model output after improvement tool was applied and each metric passed
    evaluation.
    """

    improvement_action: Literal["regen", "fixit", "do_nothing"]
    """Type of improvement action used to improve the event."""

    improvement_tool_status: Optional[Literal["improved", "failed on max retries", "improvement_required"]] = None
    """Status of the improvement tool used to improve the event."""

    status: Literal["In Progress", "Completed"]
    """Status of the event."""

    threshold_type: Literal["custom", "automatic"]
    """Type of thresholds used to evaluate the event."""

    workflow_id: str
    """Workflow ID associated with the event."""

    automatic_hallucination_tolerance_levels: Optional[Dict[str, Literal["low", "medium", "high"]]] = None
    """Mapping of guardrail metric names to tolerance values.

    Values are strings (`low`, `medium`, `high`) representing automatic tolerance
    levels.
    """

    capabilities: Optional[List[Capability]] = None
    """Extended AI capabilities available to the event, if any.

    Can be `web_search`, `context_awareness`, and/or `file_search`.
    """

    custom_hallucination_threshold_values: Optional[Dict[str, float]] = None
    """Mapping of guardrail metric names to threshold values.

    Values are floating point numbers (0.0-1.0) representing custom thresholds.
    """

    files: Optional[List[File]] = None
    """List of files available to the event, if any.

    Will only be present if `file_search` is enabled.
    """
