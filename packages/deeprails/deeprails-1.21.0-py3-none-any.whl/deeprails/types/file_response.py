# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["FileResponse"]


class FileResponse(BaseModel):
    file_id: Optional[str] = None
    """A unique file ID."""

    file_name: Optional[str] = None
    """Name of the file."""

    file_size: Optional[int] = None
    """The size of the file in bytes."""
