# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["StorageCreateParams", "Storage", "StorageAws", "StorageChunkify", "StorageCloudflare"]


class StorageCreateParams(TypedDict, total=False):
    storage: Required[Storage]
    """The parameters for creating a new storage configuration."""


class StorageAws(TypedDict, total=False):
    access_key_id: Required[str]
    """AccessKeyId is the access key for the storage provider.

    Required if not using Chunkify storage.
    """

    bucket: Required[str]
    """Bucket is the name of the storage bucket."""

    provider: Required[Literal["aws"]]
    """Provider specifies the storage provider."""

    region: Required[
        Literal[
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
    ]
    """Region specifies the region of the storage provider."""

    secret_access_key: Required[str]
    """SecretAccessKey is the secret key for the storage provider.

    Required if not using Chunkify storage.
    """

    public: bool
    """Public indicates whether the storage is publicly accessible."""


class StorageChunkify(TypedDict, total=False):
    provider: Required[Literal["chunkify"]]
    """Provider specifies the storage provider."""

    region: Required[
        Literal[
            "us-east-1",
            "us-east-2",
            "us-west-1",
            "us-west-2",
            "eu-west-1",
            "eu-west-2",
            "ap-northeast-1",
            "ap-southeast-1",
        ]
    ]
    """Region specifies the region of the storage provider."""


class StorageCloudflare(TypedDict, total=False):
    access_key_id: Required[str]
    """AccessKeyId is the access key for the storage provider."""

    bucket: Required[str]
    """Bucket is the name of the storage bucket."""

    endpoint: Required[str]
    """Endpoint is the endpoint of the storage provider."""

    location: Required[Literal["US", "EU", "ASIA"]]
    """Location specifies the location of the storage provider."""

    provider: Required[Literal["cloudflare"]]
    """Provider specifies the storage provider."""

    region: Required[Literal["auto"]]
    """Region must be set to 'auto'."""

    secret_access_key: Required[str]
    """SecretAccessKey is the secret key for the storage provider."""

    public: bool
    """Public indicates whether the storage is publicly accessible."""


Storage: TypeAlias = Union[StorageAws, StorageChunkify, StorageCloudflare]
