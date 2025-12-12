# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["LogListParams"]


class LogListParams(TypedDict, total=False):
    service: Required[Literal["transcoder", "manager"]]
    """Service type (transcoder or manager)"""

    transcoder_id: int
    """Transcoder ID (required if service is transcoder)"""
