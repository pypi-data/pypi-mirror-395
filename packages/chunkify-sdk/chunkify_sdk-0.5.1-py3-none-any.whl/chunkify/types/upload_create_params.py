# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypedDict

__all__ = ["UploadCreateParams"]


class UploadCreateParams(TypedDict, total=False):
    metadata: Dict[str, str]
    """
    Metadata allows for additional information to be attached to the upload, with a
    maximum size of 1024 bytes.
    """

    validity_timeout: int
    """The upload URL will be valid for the given timeout in seconds"""
