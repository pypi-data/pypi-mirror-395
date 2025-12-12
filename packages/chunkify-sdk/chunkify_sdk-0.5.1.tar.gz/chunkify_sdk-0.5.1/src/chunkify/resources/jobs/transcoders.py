# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.jobs.transcoder_list_response import TranscoderListResponse

__all__ = ["TranscodersResource", "AsyncTranscodersResource"]


class TranscodersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TranscodersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/chunkifydev/chunkify-python#accessing-raw-response-data-eg-headers
        """
        return TranscodersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TranscodersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/chunkifydev/chunkify-python#with_streaming_response
        """
        return TranscodersResourceWithStreamingResponse(self)

    def list(
        self,
        job_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TranscoderListResponse:
        """
        Retrieve all the transcoders statuses for a specific job

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not job_id:
            raise ValueError(f"Expected a non-empty value for `job_id` but received {job_id!r}")
        return self._get(
            f"/api/jobs/{job_id}/transcoders",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TranscoderListResponse,
        )


class AsyncTranscodersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTranscodersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/chunkifydev/chunkify-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTranscodersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTranscodersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/chunkifydev/chunkify-python#with_streaming_response
        """
        return AsyncTranscodersResourceWithStreamingResponse(self)

    async def list(
        self,
        job_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TranscoderListResponse:
        """
        Retrieve all the transcoders statuses for a specific job

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not job_id:
            raise ValueError(f"Expected a non-empty value for `job_id` but received {job_id!r}")
        return await self._get(
            f"/api/jobs/{job_id}/transcoders",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TranscoderListResponse,
        )


class TranscodersResourceWithRawResponse:
    def __init__(self, transcoders: TranscodersResource) -> None:
        self._transcoders = transcoders

        self.list = to_raw_response_wrapper(
            transcoders.list,
        )


class AsyncTranscodersResourceWithRawResponse:
    def __init__(self, transcoders: AsyncTranscodersResource) -> None:
        self._transcoders = transcoders

        self.list = async_to_raw_response_wrapper(
            transcoders.list,
        )


class TranscodersResourceWithStreamingResponse:
    def __init__(self, transcoders: TranscodersResource) -> None:
        self._transcoders = transcoders

        self.list = to_streamed_response_wrapper(
            transcoders.list,
        )


class AsyncTranscodersResourceWithStreamingResponse:
    def __init__(self, transcoders: AsyncTranscodersResource) -> None:
        self._transcoders = transcoders

        self.list = async_to_streamed_response_wrapper(
            transcoders.list,
        )
