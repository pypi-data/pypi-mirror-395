# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["SourceCreateParams"]


class SourceCreateParams(TypedDict, total=False):
    url: Required[str]
    """Url is the URL of the source, which must be a valid HTTP URL."""

    metadata: Dict[str, str]
    """
    Metadata allows for additional information to be attached to the source, with a
    maximum size of 1024 bytes.
    """
