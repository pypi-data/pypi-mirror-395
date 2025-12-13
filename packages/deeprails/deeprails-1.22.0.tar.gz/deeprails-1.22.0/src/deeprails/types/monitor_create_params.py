# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["MonitorCreateParams"]


class MonitorCreateParams(TypedDict, total=False):
    guardrail_metrics: Required[
        List[
            Literal[
                "correctness",
                "completeness",
                "instruction_adherence",
                "context_adherence",
                "ground_truth_adherence",
                "comprehensive_safety",
            ]
        ]
    ]
    """
    An array of guardrail metrics that the model input and output pair will be
    evaluated on. For non-enterprise users, these will be limited to `correctness`,
    `completeness`, `instruction_adherence`, `context_adherence`,
    `ground_truth_adherence`, and/or `comprehensive_safety`.
    """

    name: Required[str]
    """Name of the new monitor."""

    context_awareness: bool
    """
    Context includes any structured information that directly relates to the model’s
    input and expected output—e.g., the recent turn-by-turn history between an AI
    tutor and a student, facts or state passed through an agentic workflow, or other
    domain-specific signals your system already knows and wants the model to
    condition on. This field determines whether to enable context awareness for this
    monitor's evaluations. Defaults to false.
    """

    description: str
    """Description of the new monitor."""

    file_search: SequenceNotStr[str]
    """An array of file IDs to search in the monitor's evaluations.

    Files must be uploaded via the DeepRails API first.
    """

    web_search: bool
    """Whether to enable web search for this monitor's evaluations. Defaults to false."""
