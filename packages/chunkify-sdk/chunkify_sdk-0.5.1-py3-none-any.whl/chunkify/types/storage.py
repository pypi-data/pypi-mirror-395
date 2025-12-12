# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = ["Storage", "Chunkify", "Cloudflare", "Aws"]


class Chunkify(BaseModel):
    id: str
    """Unique identifier of the storage configuration"""

    created_at: datetime
    """Created at timestamp"""

    provider: Literal["chunkify"]
    """Provider specifies the storage provider."""

    region: Literal[
        "us-east-1", "us-east-2", "us-west-1", "us-west-2", "eu-west-1", "eu-west-2", "ap-northeast-1", "ap-southeast-1"
    ]
    """Region specifies the region of the storage provider."""

    slug: str
    """Unique identifier of the storage configuration"""


class Cloudflare(BaseModel):
    id: str
    """Unique identifier of the storage configuration"""

    bucket: str
    """Bucket is the name of the storage bucket."""

    created_at: datetime
    """Created at timestamp"""

    endpoint: str
    """Endpoint is the endpoint of the storage provider."""

    location: Literal["US", "EU", "ASIA"]
    """Location specifies the location of the storage provider."""

    provider: Literal["cloudflare"]
    """Provider specifies the storage provider."""

    public: bool
    """Public indicates whether the storage is publicly accessible."""

    region: Literal["auto"]
    """Region specifies the region of the storage provider."""

    slug: str
    """Unique identifier of the storage configuration"""


class Aws(BaseModel):
    id: str
    """Unique identifier of the storage configuration"""

    bucket: str
    """Bucket is the name of the storage bucket."""

    created_at: datetime
    """Created at timestamp"""

    provider: Literal["aws"]
    """Provider specifies the storage provider."""

    public: bool
    """Public indicates whether the storage is publicly accessible."""

    region: Literal[
        "us-east-1",
        "us-east-2",
        "us-central-1",
        "us-west-1",
        "us-west-2",
        "eu-west-1",
        "eu-west-2",
        "eu-west-3",
        "eu-central-1",
        "eu-north-1",
        "ap-east-1",
        "ap-east-2",
        "ap-northeast-1",
        "ap-northeast-2",
        "ap-south-1",
        "ap-southeast-1",
        "ap-southeast-2",
    ]
    """Region specifies the region of the storage provider."""

    slug: str
    """Unique identifier of the storage configuration"""


Storage: TypeAlias = Annotated[Union[Chunkify, Cloudflare, Aws], PropertyInfo(discriminator="provider")]
