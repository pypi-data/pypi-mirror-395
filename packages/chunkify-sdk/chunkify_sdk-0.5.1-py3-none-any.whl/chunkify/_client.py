# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Omit,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from .resources import files, tokens, sources, uploads, projects, storages, webhooks, notifications
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)
from .resources.jobs import jobs

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "Chunkify",
    "AsyncChunkify",
    "Client",
    "AsyncClient",
]


class Chunkify(SyncAPIClient):
    files: files.FilesResource
    jobs: jobs.JobsResource
    notifications: notifications.NotificationsResource
    projects: projects.ProjectsResource
    sources: sources.SourcesResource
    storages: storages.StoragesResource
    tokens: tokens.TokensResource
    uploads: uploads.UploadsResource
    webhooks: webhooks.WebhooksResource
    with_raw_response: ChunkifyWithRawResponse
    with_streaming_response: ChunkifyWithStreamedResponse

    # client options
    project_access_token: str | None
    team_access_token: str | None
    webhook_key: str | None

    def __init__(
        self,
        *,
        project_access_token: str | None = None,
        team_access_token: str | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Chunkify client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `project_access_token` from `CHUNKIFY_TOKEN`
        - `team_access_token` from `CHUNKIFY_TEAM_TOKEN`
        - `webhook_key` from `CHUNKIFY_WEBHOOK_SECRET`
        """
        if project_access_token is None:
            project_access_token = os.environ.get("CHUNKIFY_TOKEN")
        self.project_access_token = project_access_token

        if team_access_token is None:
            team_access_token = os.environ.get("CHUNKIFY_TEAM_TOKEN")
        self.team_access_token = team_access_token

        if webhook_key is None:
            webhook_key = os.environ.get("CHUNKIFY_WEBHOOK_SECRET")
        self.webhook_key = webhook_key

        if base_url is None:
            base_url = os.environ.get("CHUNKIFY_BASE_URL")
        if base_url is None:
            base_url = f"https://api.chunkify.dev/v1"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.files = files.FilesResource(self)
        self.jobs = jobs.JobsResource(self)
        self.notifications = notifications.NotificationsResource(self)
        self.projects = projects.ProjectsResource(self)
        self.sources = sources.SourcesResource(self)
        self.storages = storages.StoragesResource(self)
        self.tokens = tokens.TokensResource(self)
        self.uploads = uploads.UploadsResource(self)
        self.webhooks = webhooks.WebhooksResource(self)
        self.with_raw_response = ChunkifyWithRawResponse(self)
        self.with_streaming_response = ChunkifyWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="repeat")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._project_access_token, **self._team_access_token}

    @property
    def _project_access_token(self) -> dict[str, str]:
        project_access_token = self.project_access_token
        if project_access_token is None:
            return {}
        return {"Authorization": f"Bearer {project_access_token}"}

    @property
    def _team_access_token(self) -> dict[str, str]:
        team_access_token = self.team_access_token
        if team_access_token is None:
            return {}
        return {"Authorization": f"Bearer {team_access_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.project_access_token and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        if self.team_access_token and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either project_access_token or team_access_token to be set. Or for one of the `Authorization` or `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        project_access_token: str | None = None,
        team_access_token: str | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            project_access_token=project_access_token or self.project_access_token,
            team_access_token=team_access_token or self.team_access_token,
            webhook_key=webhook_key or self.webhook_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncChunkify(AsyncAPIClient):
    files: files.AsyncFilesResource
    jobs: jobs.AsyncJobsResource
    notifications: notifications.AsyncNotificationsResource
    projects: projects.AsyncProjectsResource
    sources: sources.AsyncSourcesResource
    storages: storages.AsyncStoragesResource
    tokens: tokens.AsyncTokensResource
    uploads: uploads.AsyncUploadsResource
    webhooks: webhooks.AsyncWebhooksResource
    with_raw_response: AsyncChunkifyWithRawResponse
    with_streaming_response: AsyncChunkifyWithStreamedResponse

    # client options
    project_access_token: str | None
    team_access_token: str | None
    webhook_key: str | None

    def __init__(
        self,
        *,
        project_access_token: str | None = None,
        team_access_token: str | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncChunkify client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `project_access_token` from `CHUNKIFY_TOKEN`
        - `team_access_token` from `CHUNKIFY_TEAM_TOKEN`
        - `webhook_key` from `CHUNKIFY_WEBHOOK_SECRET`
        """
        if project_access_token is None:
            project_access_token = os.environ.get("CHUNKIFY_TOKEN")
        self.project_access_token = project_access_token

        if team_access_token is None:
            team_access_token = os.environ.get("CHUNKIFY_TEAM_TOKEN")
        self.team_access_token = team_access_token

        if webhook_key is None:
            webhook_key = os.environ.get("CHUNKIFY_WEBHOOK_SECRET")
        self.webhook_key = webhook_key

        if base_url is None:
            base_url = os.environ.get("CHUNKIFY_BASE_URL")
        if base_url is None:
            base_url = f"https://api.chunkify.dev/v1"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.files = files.AsyncFilesResource(self)
        self.jobs = jobs.AsyncJobsResource(self)
        self.notifications = notifications.AsyncNotificationsResource(self)
        self.projects = projects.AsyncProjectsResource(self)
        self.sources = sources.AsyncSourcesResource(self)
        self.storages = storages.AsyncStoragesResource(self)
        self.tokens = tokens.AsyncTokensResource(self)
        self.uploads = uploads.AsyncUploadsResource(self)
        self.webhooks = webhooks.AsyncWebhooksResource(self)
        self.with_raw_response = AsyncChunkifyWithRawResponse(self)
        self.with_streaming_response = AsyncChunkifyWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="repeat")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._project_access_token, **self._team_access_token}

    @property
    def _project_access_token(self) -> dict[str, str]:
        project_access_token = self.project_access_token
        if project_access_token is None:
            return {}
        return {"Authorization": f"Bearer {project_access_token}"}

    @property
    def _team_access_token(self) -> dict[str, str]:
        team_access_token = self.team_access_token
        if team_access_token is None:
            return {}
        return {"Authorization": f"Bearer {team_access_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.project_access_token and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        if self.team_access_token and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either project_access_token or team_access_token to be set. Or for one of the `Authorization` or `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        project_access_token: str | None = None,
        team_access_token: str | None = None,
        webhook_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            project_access_token=project_access_token or self.project_access_token,
            team_access_token=team_access_token or self.team_access_token,
            webhook_key=webhook_key or self.webhook_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class ChunkifyWithRawResponse:
    def __init__(self, client: Chunkify) -> None:
        self.files = files.FilesResourceWithRawResponse(client.files)
        self.jobs = jobs.JobsResourceWithRawResponse(client.jobs)
        self.notifications = notifications.NotificationsResourceWithRawResponse(client.notifications)
        self.projects = projects.ProjectsResourceWithRawResponse(client.projects)
        self.sources = sources.SourcesResourceWithRawResponse(client.sources)
        self.storages = storages.StoragesResourceWithRawResponse(client.storages)
        self.tokens = tokens.TokensResourceWithRawResponse(client.tokens)
        self.uploads = uploads.UploadsResourceWithRawResponse(client.uploads)
        self.webhooks = webhooks.WebhooksResourceWithRawResponse(client.webhooks)


class AsyncChunkifyWithRawResponse:
    def __init__(self, client: AsyncChunkify) -> None:
        self.files = files.AsyncFilesResourceWithRawResponse(client.files)
        self.jobs = jobs.AsyncJobsResourceWithRawResponse(client.jobs)
        self.notifications = notifications.AsyncNotificationsResourceWithRawResponse(client.notifications)
        self.projects = projects.AsyncProjectsResourceWithRawResponse(client.projects)
        self.sources = sources.AsyncSourcesResourceWithRawResponse(client.sources)
        self.storages = storages.AsyncStoragesResourceWithRawResponse(client.storages)
        self.tokens = tokens.AsyncTokensResourceWithRawResponse(client.tokens)
        self.uploads = uploads.AsyncUploadsResourceWithRawResponse(client.uploads)
        self.webhooks = webhooks.AsyncWebhooksResourceWithRawResponse(client.webhooks)


class ChunkifyWithStreamedResponse:
    def __init__(self, client: Chunkify) -> None:
        self.files = files.FilesResourceWithStreamingResponse(client.files)
        self.jobs = jobs.JobsResourceWithStreamingResponse(client.jobs)
        self.notifications = notifications.NotificationsResourceWithStreamingResponse(client.notifications)
        self.projects = projects.ProjectsResourceWithStreamingResponse(client.projects)
        self.sources = sources.SourcesResourceWithStreamingResponse(client.sources)
        self.storages = storages.StoragesResourceWithStreamingResponse(client.storages)
        self.tokens = tokens.TokensResourceWithStreamingResponse(client.tokens)
        self.uploads = uploads.UploadsResourceWithStreamingResponse(client.uploads)
        self.webhooks = webhooks.WebhooksResourceWithStreamingResponse(client.webhooks)


class AsyncChunkifyWithStreamedResponse:
    def __init__(self, client: AsyncChunkify) -> None:
        self.files = files.AsyncFilesResourceWithStreamingResponse(client.files)
        self.jobs = jobs.AsyncJobsResourceWithStreamingResponse(client.jobs)
        self.notifications = notifications.AsyncNotificationsResourceWithStreamingResponse(client.notifications)
        self.projects = projects.AsyncProjectsResourceWithStreamingResponse(client.projects)
        self.sources = sources.AsyncSourcesResourceWithStreamingResponse(client.sources)
        self.storages = storages.AsyncStoragesResourceWithStreamingResponse(client.storages)
        self.tokens = tokens.AsyncTokensResourceWithStreamingResponse(client.tokens)
        self.uploads = uploads.AsyncUploadsResourceWithStreamingResponse(client.uploads)
        self.webhooks = webhooks.AsyncWebhooksResourceWithStreamingResponse(client.webhooks)


Client = Chunkify

AsyncClient = AsyncChunkify
