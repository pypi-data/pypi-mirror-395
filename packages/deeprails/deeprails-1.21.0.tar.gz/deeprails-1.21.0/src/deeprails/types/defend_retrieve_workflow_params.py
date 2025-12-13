# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["DefendRetrieveWorkflowParams"]


class DefendRetrieveWorkflowParams(TypedDict, total=False):
    limit: int
    """Limit the number of returned events associated with this workflow.

    Defaults to 10.
    """
