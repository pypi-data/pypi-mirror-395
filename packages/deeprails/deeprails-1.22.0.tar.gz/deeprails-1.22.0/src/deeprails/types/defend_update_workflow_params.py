# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, TypedDict

from .._types import SequenceNotStr

__all__ = ["DefendUpdateWorkflowParams"]


class DefendUpdateWorkflowParams(TypedDict, total=False):
    automatic_hallucination_tolerance_levels: Dict[str, Literal["low", "medium", "high"]]
    """
    New mapping of guardrail metrics to hallucination tolerance levels (either
    `low`, `medium`, or `high`) to be used when `threshold_type` is set to
    `automatic`. Possible metrics are `completeness`, `instruction_adherence`,
    `context_adherence`, `ground_truth_adherence`, or `comprehensive_safety`.
    """

    context_awareness: bool
    """Whether to enable context awareness for this workflow's evaluations."""

    custom_hallucination_threshold_values: Dict[str, float]
    """
    New mapping of guardrail metrics to floating point threshold values to be used
    when `threshold_type` is set to `custom`. Possible metrics are `correctness`,
    `completeness`, `instruction_adherence`, `context_adherence`,
    `ground_truth_adherence`, or `comprehensive_safety`.
    """

    description: str
    """New description for the workflow."""

    file_search: SequenceNotStr[str]
    """An array of file IDs to search in the workflow's evaluations.

    Files must be uploaded via the DeepRails API first.
    """

    improvement_action: Literal["regen", "fixit", "do_nothing"]
    """
    The new action used to improve outputs that fail one or more guardrail metrics
    for the workflow events. May be `regen`, `fixit`, or `do_nothing`. ReGen runs
    the user's input prompt with minor induced variance. FixIt attempts to directly
    address the shortcomings of the output using the guardrail failure rationale. Do
    Nothing does not attempt any improvement.
    """

    max_improvement_attempts: int
    """Max.

    number of improvement action attempts until a given event passes the guardrails.
    Defaults to 10.
    """

    name: str
    """New name for the workflow."""

    threshold_type: Literal["automatic", "custom"]
    """New type of thresholds to use for the workflow, either `automatic` or `custom`.

    Automatic thresholds are assigned internally after the user specifies a
    qualitative tolerance for the metrics, whereas custom metrics allow the user to
    set the threshold for each metric as a floating point number between 0.0 and
    1.0.
    """

    web_search: bool
    """Whether to enable web search for this workflow's evaluations."""
