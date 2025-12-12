# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Type, cast
from typing_extensions import Literal

import httpx

from ..types import notification_list_params, notification_create_params
from .._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
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
from ..types.notification import Notification

__all__ = ["NotificationsResource", "AsyncNotificationsResource"]


class NotificationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> NotificationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/chunkifydev/chunkify-python#accessing-raw-response-data-eg-headers
        """
        return NotificationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> NotificationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/chunkifydev/chunkify-python#with_streaming_response
        """
        return NotificationsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        event: Literal[
            "job.completed", "job.failed", "job.cancelled", "upload.completed", "upload.failed", "upload.expired"
        ],
        object_id: str,
        webhook_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Notification:
        """
        Create a new notification for a job event

        Args:
          event: Event specifies the type of event that triggered the notification.

          object_id: ObjectId specifies the object that triggered this notification.

          webhook_id: WebhookId specifies the webhook endpoint that will receive the notification.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/notifications",
            body=maybe_transform(
                {
                    "event": event,
                    "object_id": object_id,
                    "webhook_id": webhook_id,
                },
                notification_create_params.NotificationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=DataWrapper[Notification]._unwrapper,
            ),
            cast_to=cast(Type[Notification], DataWrapper[Notification]),
        )

    def retrieve(
        self,
        notification_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Notification:
        """
        Retrieve details of a specific notification

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not notification_id:
            raise ValueError(f"Expected a non-empty value for `notification_id` but received {notification_id!r}")
        return self._get(
            f"/api/notifications/{notification_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=DataWrapper[Notification]._unwrapper,
            ),
            cast_to=cast(Type[Notification], DataWrapper[Notification]),
        )

    def list(
        self,
        *,
        created: notification_list_params.Created | Omit = omit,
        events: List[
            Literal[
                "job.completed", "job.failed", "job.cancelled", "upload.completed", "upload.failed", "upload.expired"
            ]
        ]
        | Omit = omit,
        limit: int | Omit = omit,
        object_id: str | Omit = omit,
        offset: int | Omit = omit,
        response_status_code: notification_list_params.ResponseStatusCode | Omit = omit,
        webhook_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPaginatedResults[Notification]:
        """
        Retrieve a list of notifications with optional filtering and pagination

        Args:
          events: Filter by events

          limit: Pagination limit (max 100)

          object_id: Filter by object ID

          offset: Pagination offset

          webhook_id: Filter by webhook ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/notifications",
            page=SyncPaginatedResults[Notification],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "created": created,
                        "events": events,
                        "limit": limit,
                        "object_id": object_id,
                        "offset": offset,
                        "response_status_code": response_status_code,
                        "webhook_id": webhook_id,
                    },
                    notification_list_params.NotificationListParams,
                ),
            ),
            model=Notification,
        )

    def delete(
        self,
        notification_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Delete a notification.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not notification_id:
            raise ValueError(f"Expected a non-empty value for `notification_id` but received {notification_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/notifications/{notification_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncNotificationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncNotificationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/chunkifydev/chunkify-python#accessing-raw-response-data-eg-headers
        """
        return AsyncNotificationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncNotificationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/chunkifydev/chunkify-python#with_streaming_response
        """
        return AsyncNotificationsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        event: Literal[
            "job.completed", "job.failed", "job.cancelled", "upload.completed", "upload.failed", "upload.expired"
        ],
        object_id: str,
        webhook_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Notification:
        """
        Create a new notification for a job event

        Args:
          event: Event specifies the type of event that triggered the notification.

          object_id: ObjectId specifies the object that triggered this notification.

          webhook_id: WebhookId specifies the webhook endpoint that will receive the notification.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/notifications",
            body=await async_maybe_transform(
                {
                    "event": event,
                    "object_id": object_id,
                    "webhook_id": webhook_id,
                },
                notification_create_params.NotificationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=DataWrapper[Notification]._unwrapper,
            ),
            cast_to=cast(Type[Notification], DataWrapper[Notification]),
        )

    async def retrieve(
        self,
        notification_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Notification:
        """
        Retrieve details of a specific notification

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not notification_id:
            raise ValueError(f"Expected a non-empty value for `notification_id` but received {notification_id!r}")
        return await self._get(
            f"/api/notifications/{notification_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=DataWrapper[Notification]._unwrapper,
            ),
            cast_to=cast(Type[Notification], DataWrapper[Notification]),
        )

    def list(
        self,
        *,
        created: notification_list_params.Created | Omit = omit,
        events: List[
            Literal[
                "job.completed", "job.failed", "job.cancelled", "upload.completed", "upload.failed", "upload.expired"
            ]
        ]
        | Omit = omit,
        limit: int | Omit = omit,
        object_id: str | Omit = omit,
        offset: int | Omit = omit,
        response_status_code: notification_list_params.ResponseStatusCode | Omit = omit,
        webhook_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Notification, AsyncPaginatedResults[Notification]]:
        """
        Retrieve a list of notifications with optional filtering and pagination

        Args:
          events: Filter by events

          limit: Pagination limit (max 100)

          object_id: Filter by object ID

          offset: Pagination offset

          webhook_id: Filter by webhook ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/api/notifications",
            page=AsyncPaginatedResults[Notification],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "created": created,
                        "events": events,
                        "limit": limit,
                        "object_id": object_id,
                        "offset": offset,
                        "response_status_code": response_status_code,
                        "webhook_id": webhook_id,
                    },
                    notification_list_params.NotificationListParams,
                ),
            ),
            model=Notification,
        )

    async def delete(
        self,
        notification_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Delete a notification.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not notification_id:
            raise ValueError(f"Expected a non-empty value for `notification_id` but received {notification_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/notifications/{notification_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class NotificationsResourceWithRawResponse:
    def __init__(self, notifications: NotificationsResource) -> None:
        self._notifications = notifications

        self.create = to_raw_response_wrapper(
            notifications.create,
        )
        self.retrieve = to_raw_response_wrapper(
            notifications.retrieve,
        )
        self.list = to_raw_response_wrapper(
            notifications.list,
        )
        self.delete = to_raw_response_wrapper(
            notifications.delete,
        )


class AsyncNotificationsResourceWithRawResponse:
    def __init__(self, notifications: AsyncNotificationsResource) -> None:
        self._notifications = notifications

        self.create = async_to_raw_response_wrapper(
            notifications.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            notifications.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            notifications.list,
        )
        self.delete = async_to_raw_response_wrapper(
            notifications.delete,
        )


class NotificationsResourceWithStreamingResponse:
    def __init__(self, notifications: NotificationsResource) -> None:
        self._notifications = notifications

        self.create = to_streamed_response_wrapper(
            notifications.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            notifications.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            notifications.list,
        )
        self.delete = to_streamed_response_wrapper(
            notifications.delete,
        )


class AsyncNotificationsResourceWithStreamingResponse:
    def __init__(self, notifications: AsyncNotificationsResource) -> None:
        self._notifications = notifications

        self.create = async_to_streamed_response_wrapper(
            notifications.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            notifications.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            notifications.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            notifications.delete,
        )
