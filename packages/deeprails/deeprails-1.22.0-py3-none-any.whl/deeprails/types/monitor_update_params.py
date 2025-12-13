# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

from .._types import SequenceNotStr

__all__ = ["MonitorUpdateParams"]


class MonitorUpdateParams(TypedDict, total=False):
    description: str
    """New description of the monitor."""

    file_search: SequenceNotStr[str]
    """An array of file IDs to search in the monitor's evaluations.

    Files must be uploaded via the DeepRails API first.
    """

    guardrail_metrics: List[
        Literal[
            "correctness",
            "completeness",
            "instruction_adherence",
            "context_adherence",
            "ground_truth_adherence",
            "comprehensive_safety",
        ]
    ]
    """
    An array of the new guardrail metrics that model input and output pairs will be
    evaluated on.
    """

    name: str
    """New name of the monitor."""

    status: Literal["active", "inactive"]
    """Status of the monitor.

    Can be `active` or `inactive`. Inactive monitors no longer record and evaluate
    events.
    """

    web_search: bool
    """Whether to enable web search for this monitor's evaluations."""
