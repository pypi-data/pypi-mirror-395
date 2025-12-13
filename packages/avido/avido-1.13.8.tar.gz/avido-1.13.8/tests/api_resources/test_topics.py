# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from avido import Avido, AsyncAvido
from avido.types import Topic, TopicResponse
from tests.utils import assert_matches_type
from avido.pagination import SyncOffsetPagination, AsyncOffsetPagination

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTopics:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Avido) -> None:
        topic = client.topics.create(
            title="Code Quality",
        )
        assert_matches_type(TopicResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Avido) -> None:
        topic = client.topics.create(
            title="Code Quality",
            baseline=0.85,
        )
        assert_matches_type(TopicResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Avido) -> None:
        response = client.topics.with_raw_response.create(
            title="Code Quality",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = response.parse()
        assert_matches_type(TopicResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Avido) -> None:
        with client.topics.with_streaming_response.create(
            title="Code Quality",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = response.parse()
            assert_matches_type(TopicResponse, topic, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Avido) -> None:
        topic = client.topics.retrieve(
            "789e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(TopicResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Avido) -> None:
        response = client.topics.with_raw_response.retrieve(
            "789e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = response.parse()
        assert_matches_type(TopicResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Avido) -> None:
        with client.topics.with_streaming_response.retrieve(
            "789e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = response.parse()
            assert_matches_type(TopicResponse, topic, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Avido) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.topics.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Avido) -> None:
        topic = client.topics.list()
        assert_matches_type(SyncOffsetPagination[Topic], topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Avido) -> None:
        topic = client.topics.list(
            limit=25,
            order_by="createdAt",
            order_dir="desc",
            skip=0,
            title="code quality",
        )
        assert_matches_type(SyncOffsetPagination[Topic], topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Avido) -> None:
        response = client.topics.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = response.parse()
        assert_matches_type(SyncOffsetPagination[Topic], topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Avido) -> None:
        with client.topics.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = response.parse()
            assert_matches_type(SyncOffsetPagination[Topic], topic, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTopics:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncAvido) -> None:
        topic = await async_client.topics.create(
            title="Code Quality",
        )
        assert_matches_type(TopicResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAvido) -> None:
        topic = await async_client.topics.create(
            title="Code Quality",
            baseline=0.85,
        )
        assert_matches_type(TopicResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAvido) -> None:
        response = await async_client.topics.with_raw_response.create(
            title="Code Quality",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = await response.parse()
        assert_matches_type(TopicResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAvido) -> None:
        async with async_client.topics.with_streaming_response.create(
            title="Code Quality",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = await response.parse()
            assert_matches_type(TopicResponse, topic, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAvido) -> None:
        topic = await async_client.topics.retrieve(
            "789e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(TopicResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAvido) -> None:
        response = await async_client.topics.with_raw_response.retrieve(
            "789e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = await response.parse()
        assert_matches_type(TopicResponse, topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAvido) -> None:
        async with async_client.topics.with_streaming_response.retrieve(
            "789e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = await response.parse()
            assert_matches_type(TopicResponse, topic, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAvido) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.topics.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncAvido) -> None:
        topic = await async_client.topics.list()
        assert_matches_type(AsyncOffsetPagination[Topic], topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAvido) -> None:
        topic = await async_client.topics.list(
            limit=25,
            order_by="createdAt",
            order_dir="desc",
            skip=0,
            title="code quality",
        )
        assert_matches_type(AsyncOffsetPagination[Topic], topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAvido) -> None:
        response = await async_client.topics.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = await response.parse()
        assert_matches_type(AsyncOffsetPagination[Topic], topic, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAvido) -> None:
        async with async_client.topics.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = await response.parse()
            assert_matches_type(AsyncOffsetPagination[Topic], topic, path=["response"])

        assert cast(Any, response.is_closed) is True
