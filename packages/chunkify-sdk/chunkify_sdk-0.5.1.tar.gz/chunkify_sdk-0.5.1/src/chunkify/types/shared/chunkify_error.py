# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ChunkifyError"]


class ChunkifyError(BaseModel):
    detail: str
    """Additional error details or output"""

    message: str
    """Main error message"""

    type: Literal[
        "setup",
        "ffmpeg",
        "source",
        "upload",
        "download",
        "ingest",
        "job",
        "unexpected",
        "permission",
        "timeout",
        "cancelled",
    ]
    """Type of error"""
