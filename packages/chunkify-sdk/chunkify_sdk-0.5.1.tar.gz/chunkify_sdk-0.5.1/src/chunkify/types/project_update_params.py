# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ProjectUpdateParams"]


class ProjectUpdateParams(TypedDict, total=False):
    name: str
    """Name is the name of the project. Required when storage_id is not provided."""

    storage_id: str
    """StorageId is the storage id of the project. Required when name is not provided."""
