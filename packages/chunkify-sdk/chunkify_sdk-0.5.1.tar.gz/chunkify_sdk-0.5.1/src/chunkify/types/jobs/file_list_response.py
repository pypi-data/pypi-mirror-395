# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from ..._models import BaseModel
from ..api_file import APIFile

__all__ = ["FileListResponse"]


class FileListResponse(BaseModel):
    data: List[APIFile]

    status: Literal["success"]
    """Status indicates the response status "success" """
