# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, cast

import httpx

from ..types import storage_create_params
from .._types import Body, Query, Headers, NoneType, NotGiven, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._wrappers import DataWrapper
from .._base_client import make_request_options
from ..types.storage import Storage
from ..types.storage_list_response import StorageListResponse

__all__ = ["StoragesResource", "AsyncStoragesResource"]


class StoragesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> StoragesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/chunkifydev/chunkify-python#accessing-raw-response-data-eg-headers
        """
        return StoragesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> StoragesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/chunkifydev/chunkify-python#with_streaming_response
        """
        return StoragesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        storage: storage_create_params.Storage,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Storage:
        """
        Create a new storage configuration for cloud storage providers like AWS S3,
        Cloudflare R2, etc. The storage credentials will be validated before saving.

        Args:
          storage: The parameters for creating a new storage configuration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            Storage,
            self._post(
                "/api/storages",
                body=maybe_transform(storage, storage_create_params.StorageCreateParams),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    post_parser=DataWrapper[Storage]._unwrapper,
                ),
                cast_to=cast(
                    Any, DataWrapper[Storage]
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def retrieve(
        self,
        storage_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Storage:
        """
        Retrieve details of a specific storage configuration by its id.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not storage_id:
            raise ValueError(f"Expected a non-empty value for `storage_id` but received {storage_id!r}")
        return cast(
            Storage,
            self._get(
                f"/api/storages/{storage_id}",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    post_parser=DataWrapper[Storage]._unwrapper,
                ),
                cast_to=cast(
                    Any, DataWrapper[Storage]
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StorageListResponse:
        """Retrieve a list of all storage configurations for the current project."""
        return self._get(
            "/api/storages",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StorageListResponse,
        )

    def delete(
        self,
        storage_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Delete a storage configuration.

        The storage must not be currently attached to
        the project.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not storage_id:
            raise ValueError(f"Expected a non-empty value for `storage_id` but received {storage_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/storages/{storage_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncStoragesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncStoragesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/chunkifydev/chunkify-python#accessing-raw-response-data-eg-headers
        """
        return AsyncStoragesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncStoragesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/chunkifydev/chunkify-python#with_streaming_response
        """
        return AsyncStoragesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        storage: storage_create_params.Storage,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Storage:
        """
        Create a new storage configuration for cloud storage providers like AWS S3,
        Cloudflare R2, etc. The storage credentials will be validated before saving.

        Args:
          storage: The parameters for creating a new storage configuration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            Storage,
            await self._post(
                "/api/storages",
                body=await async_maybe_transform(storage, storage_create_params.StorageCreateParams),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    post_parser=DataWrapper[Storage]._unwrapper,
                ),
                cast_to=cast(
                    Any, DataWrapper[Storage]
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def retrieve(
        self,
        storage_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Storage:
        """
        Retrieve details of a specific storage configuration by its id.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not storage_id:
            raise ValueError(f"Expected a non-empty value for `storage_id` but received {storage_id!r}")
        return cast(
            Storage,
            await self._get(
                f"/api/storages/{storage_id}",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    post_parser=DataWrapper[Storage]._unwrapper,
                ),
                cast_to=cast(
                    Any, DataWrapper[Storage]
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StorageListResponse:
        """Retrieve a list of all storage configurations for the current project."""
        return await self._get(
            "/api/storages",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StorageListResponse,
        )

    async def delete(
        self,
        storage_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Delete a storage configuration.

        The storage must not be currently attached to
        the project.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not storage_id:
            raise ValueError(f"Expected a non-empty value for `storage_id` but received {storage_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/storages/{storage_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class StoragesResourceWithRawResponse:
    def __init__(self, storages: StoragesResource) -> None:
        self._storages = storages

        self.create = to_raw_response_wrapper(
            storages.create,
        )
        self.retrieve = to_raw_response_wrapper(
            storages.retrieve,
        )
        self.list = to_raw_response_wrapper(
            storages.list,
        )
        self.delete = to_raw_response_wrapper(
            storages.delete,
        )


class AsyncStoragesResourceWithRawResponse:
    def __init__(self, storages: AsyncStoragesResource) -> None:
        self._storages = storages

        self.create = async_to_raw_response_wrapper(
            storages.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            storages.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            storages.list,
        )
        self.delete = async_to_raw_response_wrapper(
            storages.delete,
        )


class StoragesResourceWithStreamingResponse:
    def __init__(self, storages: StoragesResource) -> None:
        self._storages = storages

        self.create = to_streamed_response_wrapper(
            storages.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            storages.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            storages.list,
        )
        self.delete = to_streamed_response_wrapper(
            storages.delete,
        )


class AsyncStoragesResourceWithStreamingResponse:
    def __init__(self, storages: AsyncStoragesResource) -> None:
        self._storages = storages

        self.create = async_to_streamed_response_wrapper(
            storages.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            storages.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            storages.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            storages.delete,
        )
