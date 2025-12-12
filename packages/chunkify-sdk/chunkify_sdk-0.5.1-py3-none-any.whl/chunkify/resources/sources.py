# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Type, Iterable, cast
from typing_extensions import Literal

import httpx

from ..types import source_list_params, source_create_params
from .._types import Body, Omit, Query, Headers, NoneType, NotGiven, SequenceNotStr, omit, not_given
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
from ..pagination import SyncPaginatedResults, AsyncPaginatedResults
from .._base_client import AsyncPaginator, make_request_options
from ..types.source import Source

__all__ = ["SourcesResource", "AsyncSourcesResource"]


class SourcesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SourcesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/chunkifydev/chunkify-python#accessing-raw-response-data-eg-headers
        """
        return SourcesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SourcesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/chunkifydev/chunkify-python#with_streaming_response
        """
        return SourcesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        url: str,
        metadata: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Source:
        """Create a new source from a media URL.

        The source will be analyzed to extract
        metadata and generate a thumbnail. The source will be automatically deleted
        after the data retention period.

        Args:
          url: Url is the URL of the source, which must be a valid HTTP URL.

          metadata: Metadata allows for additional information to be attached to the source, with a
              maximum size of 1024 bytes.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/sources",
            body=maybe_transform(
                {
                    "url": url,
                    "metadata": metadata,
                },
                source_create_params.SourceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=DataWrapper[Source]._unwrapper,
            ),
            cast_to=cast(Type[Source], DataWrapper[Source]),
        )

    def retrieve(
        self,
        source_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Source:
        """
        Retrieve details of a specific source by its ID, including metadata, media
        properties, and associated jobs.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not source_id:
            raise ValueError(f"Expected a non-empty value for `source_id` but received {source_id!r}")
        return self._get(
            f"/api/sources/{source_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=DataWrapper[Source]._unwrapper,
            ),
            cast_to=cast(Type[Source], DataWrapper[Source]),
        )

    def list(
        self,
        *,
        id: str | Omit = omit,
        audio_codec: str | Omit = omit,
        created: source_list_params.Created | Omit = omit,
        device: Literal["apple", "android", "unknown"] | Omit = omit,
        duration: source_list_params.Duration | Omit = omit,
        height: source_list_params.Height | Omit = omit,
        limit: int | Omit = omit,
        metadata: Iterable[SequenceNotStr[str]] | Omit = omit,
        offset: int | Omit = omit,
        size: source_list_params.Size | Omit = omit,
        video_codec: str | Omit = omit,
        width: source_list_params.Width | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPaginatedResults[Source]:
        """Retrieve a list of all sources with optional filtering and pagination.

        Supports
        filtering by various media properties like duration, dimensions, codecs, etc.

        Args:
          id: Filter by source ID

          audio_codec: Filter by audio codec

          device: Filter by device (apple/android)

          limit: Pagination limit (max 100)

          metadata: Filter by metadata

          offset: Pagination offset

          video_codec: Filter by video codec

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/sources",
            page=SyncPaginatedResults[Source],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "id": id,
                        "audio_codec": audio_codec,
                        "created": created,
                        "device": device,
                        "duration": duration,
                        "height": height,
                        "limit": limit,
                        "metadata": metadata,
                        "offset": offset,
                        "size": size,
                        "video_codec": video_codec,
                        "width": width,
                    },
                    source_list_params.SourceListParams,
                ),
            ),
            model=Source,
        )

    def delete(
        self,
        source_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Delete a source.

        It will fail if there are processing jobs using this source.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not source_id:
            raise ValueError(f"Expected a non-empty value for `source_id` but received {source_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/sources/{source_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncSourcesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSourcesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/chunkifydev/chunkify-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSourcesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSourcesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/chunkifydev/chunkify-python#with_streaming_response
        """
        return AsyncSourcesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        url: str,
        metadata: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Source:
        """Create a new source from a media URL.

        The source will be analyzed to extract
        metadata and generate a thumbnail. The source will be automatically deleted
        after the data retention period.

        Args:
          url: Url is the URL of the source, which must be a valid HTTP URL.

          metadata: Metadata allows for additional information to be attached to the source, with a
              maximum size of 1024 bytes.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/sources",
            body=await async_maybe_transform(
                {
                    "url": url,
                    "metadata": metadata,
                },
                source_create_params.SourceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=DataWrapper[Source]._unwrapper,
            ),
            cast_to=cast(Type[Source], DataWrapper[Source]),
        )

    async def retrieve(
        self,
        source_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Source:
        """
        Retrieve details of a specific source by its ID, including metadata, media
        properties, and associated jobs.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not source_id:
            raise ValueError(f"Expected a non-empty value for `source_id` but received {source_id!r}")
        return await self._get(
            f"/api/sources/{source_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=DataWrapper[Source]._unwrapper,
            ),
            cast_to=cast(Type[Source], DataWrapper[Source]),
        )

    def list(
        self,
        *,
        id: str | Omit = omit,
        audio_codec: str | Omit = omit,
        created: source_list_params.Created | Omit = omit,
        device: Literal["apple", "android", "unknown"] | Omit = omit,
        duration: source_list_params.Duration | Omit = omit,
        height: source_list_params.Height | Omit = omit,
        limit: int | Omit = omit,
        metadata: Iterable[SequenceNotStr[str]] | Omit = omit,
        offset: int | Omit = omit,
        size: source_list_params.Size | Omit = omit,
        video_codec: str | Omit = omit,
        width: source_list_params.Width | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Source, AsyncPaginatedResults[Source]]:
        """Retrieve a list of all sources with optional filtering and pagination.

        Supports
        filtering by various media properties like duration, dimensions, codecs, etc.

        Args:
          id: Filter by source ID

          audio_codec: Filter by audio codec

          device: Filter by device (apple/android)

          limit: Pagination limit (max 100)

          metadata: Filter by metadata

          offset: Pagination offset

          video_codec: Filter by video codec

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/sources",
            page=AsyncPaginatedResults[Source],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "id": id,
                        "audio_codec": audio_codec,
                        "created": created,
                        "device": device,
                        "duration": duration,
                        "height": height,
                        "limit": limit,
                        "metadata": metadata,
                        "offset": offset,
                        "size": size,
                        "video_codec": video_codec,
                        "width": width,
                    },
                    source_list_params.SourceListParams,
                ),
            ),
            model=Source,
        )

    async def delete(
        self,
        source_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Delete a source.

        It will fail if there are processing jobs using this source.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not source_id:
            raise ValueError(f"Expected a non-empty value for `source_id` but received {source_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/sources/{source_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class SourcesResourceWithRawResponse:
    def __init__(self, sources: SourcesResource) -> None:
        self._sources = sources

        self.create = to_raw_response_wrapper(
            sources.create,
        )
        self.retrieve = to_raw_response_wrapper(
            sources.retrieve,
        )
        self.list = to_raw_response_wrapper(
            sources.list,
        )
        self.delete = to_raw_response_wrapper(
            sources.delete,
        )


class AsyncSourcesResourceWithRawResponse:
    def __init__(self, sources: AsyncSourcesResource) -> None:
        self._sources = sources

        self.create = async_to_raw_response_wrapper(
            sources.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            sources.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            sources.list,
        )
        self.delete = async_to_raw_response_wrapper(
            sources.delete,
        )


class SourcesResourceWithStreamingResponse:
    def __init__(self, sources: SourcesResource) -> None:
        self._sources = sources

        self.create = to_streamed_response_wrapper(
            sources.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            sources.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            sources.list,
        )
        self.delete = to_streamed_response_wrapper(
            sources.delete,
        )


class AsyncSourcesResourceWithStreamingResponse:
    def __init__(self, sources: AsyncSourcesResource) -> None:
        self._sources = sources

        self.create = async_to_streamed_response_wrapper(
            sources.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            sources.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            sources.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            sources.delete,
        )
