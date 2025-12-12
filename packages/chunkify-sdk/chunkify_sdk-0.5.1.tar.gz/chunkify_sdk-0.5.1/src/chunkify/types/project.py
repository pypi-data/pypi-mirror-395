# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from .._models import BaseModel

__all__ = ["Project"]


class Project(BaseModel):
    id: str
    """Id is the unique identifier for the project."""

    created_at: datetime
    """Timestamp when the project was created"""

    name: str
    """Name of the project"""

    slug: str
    """Slug is the slug for the project."""

    storage_id: str
    """StorageId identifier where project files are stored"""
