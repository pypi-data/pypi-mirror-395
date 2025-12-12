# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .storage import Storage
from .._models import BaseModel

__all__ = ["StorageListResponse"]


class StorageListResponse(BaseModel):
    data: List[Storage]

    status: str
    """Status indicates the response status "success" """
