# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast
from datetime import datetime, timezone

import pytest
import standardwebhooks

from chunkify import Chunkify, AsyncChunkify
from tests.utils import assert_matches_type
from chunkify.types import Webhook, WebhookListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWebhooks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Chunkify) -> None:
        webhook = client.webhooks.create(
            url="https://example.com/webhook",
        )
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Chunkify) -> None:
        webhook = client.webhooks.create(
            url="https://example.com/webhook",
            enabled=True,
            events=["job.completed"],
        )
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Chunkify) -> None:
        response = client.webhooks.with_raw_response.create(
            url="https://example.com/webhook",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Chunkify) -> None:
        with client.webhooks.with_streaming_response.create(
            url="https://example.com/webhook",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(Webhook, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Chunkify) -> None:
        webhook = client.webhooks.retrieve(
            "webhookId",
        )
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Chunkify) -> None:
        response = client.webhooks.with_raw_response.retrieve(
            "webhookId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Chunkify) -> None:
        with client.webhooks.with_streaming_response.retrieve(
            "webhookId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(Webhook, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Chunkify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            client.webhooks.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update(self, client: Chunkify) -> None:
        webhook = client.webhooks.update(
            webhook_id="webhookId",
        )
        assert webhook is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: Chunkify) -> None:
        webhook = client.webhooks.update(
            webhook_id="webhookId",
            enabled=True,
            events=["job.completed"],
        )
        assert webhook is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: Chunkify) -> None:
        response = client.webhooks.with_raw_response.update(
            webhook_id="webhookId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert webhook is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: Chunkify) -> None:
        with client.webhooks.with_streaming_response.update(
            webhook_id="webhookId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert webhook is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_update(self, client: Chunkify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            client.webhooks.with_raw_response.update(
                webhook_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Chunkify) -> None:
        webhook = client.webhooks.list()
        assert_matches_type(WebhookListResponse, webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Chunkify) -> None:
        response = client.webhooks.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(WebhookListResponse, webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Chunkify) -> None:
        with client.webhooks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(WebhookListResponse, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete(self, client: Chunkify) -> None:
        webhook = client.webhooks.delete(
            "webhookId",
        )
        assert webhook is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Chunkify) -> None:
        response = client.webhooks.with_raw_response.delete(
            "webhookId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert webhook is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Chunkify) -> None:
        with client.webhooks.with_streaming_response.delete(
            "webhookId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert webhook is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Chunkify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            client.webhooks.with_raw_response.delete(
                "",
            )

    def test_method_unwrap(self, client: Chunkify) -> None:
        key = b"secret"
        hook = standardwebhooks.Webhook(key)

        data = """{"id":"notf_2G6MJiNz71bHQGNzGwKx5cJwPFS","data":{"files":[{"id":"file_2G6MJiNz71bHQGNzGwKx5cJwPFS","audio_bitrate":128000,"audio_codec":"aac","created_at":"2025-01-01T12:00:00Z","duration":120,"height":1080,"job_id":"job_2G6MJiNz71bHQGNzGwKx5cJwPFS","mime_type":"video/mp4","path":"path/to/file.mp4","size":1234567,"storage_id":"stor_chunkify_2wLmj1fp8neUaFAWwwxvzKAT0Fa","url":"https://my-bucket.s3.us-east-1.amazonaws.com/path/to/file.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256","video_bitrate":20000000,"video_codec":"h264","video_framerate":29.97,"width":1920}],"job":{"id":"job_2G6MJiNz71bHQGNzGwKx5cJwPFS","billable_time":120,"created_at":"2025-01-01T12:00:00Z","format":{"id":"mp4_h264","audio_bitrate":32000,"bufsize":100000,"channels":1,"crf":35,"disable_audio":true,"disable_video":true,"duration":1,"framerate":15,"gop":1,"height":-2,"level":41,"maxrate":100000,"minrate":100000,"movflags":"movflags","pixfmt":"yuv410p","preset":"10","profilev":"main10","seek":1,"video_bitrate":100000,"width":-2},"progress":45.5,"source_id":"src_2G6MJiNz71bHQGNzGwKx5cJwPFS","status":"transcoding","storage":{"id":"stor_aws_S1cce6120E56e7Tu9ioP09Nhjk1","path":"path/to/video.mp4"},"transcoder":{"auto":true,"quantity":10,"type":"4vCPU"},"updated_at":"2025-01-01T12:05:00Z","error":{"detail":"detail","message":"message","type":"setup"},"hls_manifest_id":"hls_2v6EIgcNAycdS5g0IUm0TXBjvHV","metadata":{"key1":"value1","key2":"value2"},"started_at":"2025-01-01T12:01:00Z"}},"date":"2025-01-01T12:00:00Z","event":"job.completed"}"""
        msg_id = "1"
        timestamp = datetime.now(tz=timezone.utc)
        sig = hook.sign(msg_id=msg_id, timestamp=timestamp, data=data)
        headers = {
            "webhook-id": msg_id,
            "webhook-timestamp": str(int(timestamp.timestamp())),
            "webhook-signature": sig,
        }

        try:
            _ = client.webhooks.unwrap(data, headers=headers, key=key)
        except standardwebhooks.WebhookVerificationError as e:
            raise AssertionError("Failed to unwrap valid webhook") from e

        bad_headers = [
            {**headers, "webhook-signature": hook.sign(msg_id=msg_id, timestamp=timestamp, data="xxx")},
            {**headers, "webhook-id": "bad"},
            {**headers, "webhook-timestamp": "0"},
        ]
        for bad_header in bad_headers:
            with pytest.raises(standardwebhooks.WebhookVerificationError):
                _ = client.webhooks.unwrap(data, headers=bad_header, key=key)


class TestAsyncWebhooks:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncChunkify) -> None:
        webhook = await async_client.webhooks.create(
            url="https://example.com/webhook",
        )
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncChunkify) -> None:
        webhook = await async_client.webhooks.create(
            url="https://example.com/webhook",
            enabled=True,
            events=["job.completed"],
        )
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncChunkify) -> None:
        response = await async_client.webhooks.with_raw_response.create(
            url="https://example.com/webhook",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncChunkify) -> None:
        async with async_client.webhooks.with_streaming_response.create(
            url="https://example.com/webhook",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(Webhook, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncChunkify) -> None:
        webhook = await async_client.webhooks.retrieve(
            "webhookId",
        )
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncChunkify) -> None:
        response = await async_client.webhooks.with_raw_response.retrieve(
            "webhookId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(Webhook, webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncChunkify) -> None:
        async with async_client.webhooks.with_streaming_response.retrieve(
            "webhookId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(Webhook, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncChunkify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            await async_client.webhooks.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncChunkify) -> None:
        webhook = await async_client.webhooks.update(
            webhook_id="webhookId",
        )
        assert webhook is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncChunkify) -> None:
        webhook = await async_client.webhooks.update(
            webhook_id="webhookId",
            enabled=True,
            events=["job.completed"],
        )
        assert webhook is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncChunkify) -> None:
        response = await async_client.webhooks.with_raw_response.update(
            webhook_id="webhookId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert webhook is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncChunkify) -> None:
        async with async_client.webhooks.with_streaming_response.update(
            webhook_id="webhookId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert webhook is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncChunkify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            await async_client.webhooks.with_raw_response.update(
                webhook_id="",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncChunkify) -> None:
        webhook = await async_client.webhooks.list()
        assert_matches_type(WebhookListResponse, webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncChunkify) -> None:
        response = await async_client.webhooks.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(WebhookListResponse, webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncChunkify) -> None:
        async with async_client.webhooks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(WebhookListResponse, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncChunkify) -> None:
        webhook = await async_client.webhooks.delete(
            "webhookId",
        )
        assert webhook is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncChunkify) -> None:
        response = await async_client.webhooks.with_raw_response.delete(
            "webhookId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert webhook is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncChunkify) -> None:
        async with async_client.webhooks.with_streaming_response.delete(
            "webhookId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert webhook is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncChunkify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            await async_client.webhooks.with_raw_response.delete(
                "",
            )

    def test_method_unwrap(self, client: Chunkify) -> None:
        key = b"secret"
        hook = standardwebhooks.Webhook(key)

        data = """{"id":"notf_2G6MJiNz71bHQGNzGwKx5cJwPFS","data":{"files":[{"id":"file_2G6MJiNz71bHQGNzGwKx5cJwPFS","audio_bitrate":128000,"audio_codec":"aac","created_at":"2025-01-01T12:00:00Z","duration":120,"height":1080,"job_id":"job_2G6MJiNz71bHQGNzGwKx5cJwPFS","mime_type":"video/mp4","path":"path/to/file.mp4","size":1234567,"storage_id":"stor_chunkify_2wLmj1fp8neUaFAWwwxvzKAT0Fa","url":"https://my-bucket.s3.us-east-1.amazonaws.com/path/to/file.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256","video_bitrate":20000000,"video_codec":"h264","video_framerate":29.97,"width":1920}],"job":{"id":"job_2G6MJiNz71bHQGNzGwKx5cJwPFS","billable_time":120,"created_at":"2025-01-01T12:00:00Z","format":{"id":"mp4_h264","audio_bitrate":32000,"bufsize":100000,"channels":1,"crf":35,"disable_audio":true,"disable_video":true,"duration":1,"framerate":15,"gop":1,"height":-2,"level":41,"maxrate":100000,"minrate":100000,"movflags":"movflags","pixfmt":"yuv410p","preset":"10","profilev":"main10","seek":1,"video_bitrate":100000,"width":-2},"progress":45.5,"source_id":"src_2G6MJiNz71bHQGNzGwKx5cJwPFS","status":"transcoding","storage":{"id":"stor_aws_S1cce6120E56e7Tu9ioP09Nhjk1","path":"path/to/video.mp4"},"transcoder":{"auto":true,"quantity":10,"type":"4vCPU"},"updated_at":"2025-01-01T12:05:00Z","error":{"detail":"detail","message":"message","type":"setup"},"hls_manifest_id":"hls_2v6EIgcNAycdS5g0IUm0TXBjvHV","metadata":{"key1":"value1","key2":"value2"},"started_at":"2025-01-01T12:01:00Z"}},"date":"2025-01-01T12:00:00Z","event":"job.completed"}"""
        msg_id = "1"
        timestamp = datetime.now(tz=timezone.utc)
        sig = hook.sign(msg_id=msg_id, timestamp=timestamp, data=data)
        headers = {
            "webhook-id": msg_id,
            "webhook-timestamp": str(int(timestamp.timestamp())),
            "webhook-signature": sig,
        }

        try:
            _ = client.webhooks.unwrap(data, headers=headers, key=key)
        except standardwebhooks.WebhookVerificationError as e:
            raise AssertionError("Failed to unwrap valid webhook") from e

        bad_headers = [
            {**headers, "webhook-signature": hook.sign(msg_id=msg_id, timestamp=timestamp, data="xxx")},
            {**headers, "webhook-id": "bad"},
            {**headers, "webhook-timestamp": "0"},
        ]
        for bad_header in bad_headers:
            with pytest.raises(standardwebhooks.WebhookVerificationError):
                _ = client.webhooks.unwrap(data, headers=bad_header, key=key)
