# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["FileUploadParams"]


class FileUploadParams(TypedDict, total=False):
    files: Required[SequenceNotStr[str]]
    """The contents of the files to upload."""
