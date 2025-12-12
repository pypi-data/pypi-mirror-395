# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["LogListResponse", "Data"]


class Data(BaseModel):
    attributes: Dict[str, object]
    """Additional structured data attached to the log"""

    level: Literal["info", "error", "debug"]
    """Log level"""

    msg: str
    """The log message content"""

    service: Literal["transcoder", "manager"]
    """Name of the service that generated the log"""

    time: datetime
    """Timestamp when the log was created"""

    job_id: Optional[str] = None
    """Optional ID of the job this log is associated with"""


class LogListResponse(BaseModel):
    data: List[Data]

    status: str
    """Status indicates the response status "success" """
