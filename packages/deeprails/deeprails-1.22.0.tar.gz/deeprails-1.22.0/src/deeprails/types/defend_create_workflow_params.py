# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["DefendCreateWorkflowParams"]


class DefendCreateWorkflowParams(TypedDict, total=False):
    improvement_action: Required[Literal["regen", "fixit", "do_nothing"]]
    """
    The action used to improve outputs that fail one or more guardrail metrics for
    the workflow events. May be `regen`, `fixit`, or `do_nothing`. ReGen runs the
    user's input prompt with minor induced variance. FixIt attempts to directly
    address the shortcomings of the output using the guardrail failure rationale. Do
    Nothing does not attempt any improvement.
    """

    name: Required[str]
    """Name of the workflow."""

    threshold_type: Required[Literal["automatic", "custom"]]
    """Type of thresholds to use for the workflow, either `automatic` or `custom`.

    Automatic thresholds are assigned internally after the user specifies a
    qualitative tolerance for the metrics, whereas custom metrics allow the user to
    set the threshold for each metric as a floating point number between 0.0 and
    1.0.
    """

    automatic_hallucination_tolerance_levels: Dict[str, Literal["low", "medium", "high"]]
    """
    Mapping of guardrail metrics to hallucination tolerance levels (either `low`,
    `medium`, or `high`). Possible metrics are `completeness`,
    `instruction_adherence`, `context_adherence`, `ground_truth_adherence`, or
    `comprehensive_safety`.
    """

    context_awareness: bool
    """
    Context includes any structured information that directly relates to the model’s
    input and expected output—e.g., the recent turn-by-turn history between an AI
    tutor and a student, facts or state passed through an agentic workflow, or other
    domain-specific signals your system already knows and wants the model to
    condition on. This field determines whether to enable context awareness for this
    workflow's evaluations. Defaults to false.
    """

    custom_hallucination_threshold_values: Dict[str, float]
    """Mapping of guardrail metrics to floating point threshold values.

    Possible metrics are `correctness`, `completeness`, `instruction_adherence`,
    `context_adherence`, `ground_truth_adherence`, or `comprehensive_safety`.
    """

    description: str
    """Description for the workflow."""

    file_search: SequenceNotStr[str]
    """An array of file IDs to search in the workflow's evaluations.

    Files must be uploaded via the DeepRails API first.
    """

    max_improvement_attempts: int
    """Max.

    number of improvement action attempts until a given event passes the guardrails.
    Defaults to 10.
    """

    web_search: bool
    """Whether to enable web search for this workflow's evaluations.

    Defaults to false.
    """
