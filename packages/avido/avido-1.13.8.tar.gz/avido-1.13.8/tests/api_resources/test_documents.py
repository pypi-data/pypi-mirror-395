# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from avido import Avido, AsyncAvido
from avido.types import (
    DocumentChunk,
    DocumentResponse,
    DocumentListResponse,
)
from tests.utils import assert_matches_type
from avido._utils import parse_datetime
from avido.pagination import SyncOffsetPagination, AsyncOffsetPagination

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDocuments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Avido) -> None:
        document = client.documents.create(
            assignee="user_123456789",
            content="This document describes the API endpoints...",
            title="API Documentation",
        )
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Avido) -> None:
        document = client.documents.create(
            assignee="user_123456789",
            content="This document describes the API endpoints...",
            title="API Documentation",
            language="english",
            metadata={"foo": "bar"},
            original_sentences=["This is the first sentence.", "This is the second sentence."],
            scrape_job_id="321e4567-e89b-12d3-a456-426614174000",
            status="DRAFT",
        )
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Avido) -> None:
        response = client.documents.with_raw_response.create(
            assignee="user_123456789",
            content="This document describes the API endpoints...",
            title="API Documentation",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Avido) -> None:
        with client.documents.with_streaming_response.create(
            assignee="user_123456789",
            content="This document describes the API endpoints...",
            title="API Documentation",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(DocumentResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Avido) -> None:
        document = client.documents.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Avido) -> None:
        response = client.documents.with_raw_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Avido) -> None:
        with client.documents.with_streaming_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(DocumentResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Avido) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.documents.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Avido) -> None:
        document = client.documents.list()
        assert_matches_type(SyncOffsetPagination[DocumentListResponse], document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Avido) -> None:
        document = client.documents.list(
            assignee="user_123456789",
            end_date=parse_datetime("2024-12-31T23:59:59.999Z"),
            limit=25,
            order_by="createdAt",
            order_dir="desc",
            scrape_job_id="321e4567-e89b-12d3-a456-426614174000",
            search="API documentation",
            skip=0,
            start_date=parse_datetime("2024-01-01T00:00:00.000Z"),
            status="APPROVED",
            tag_id=["string"],
        )
        assert_matches_type(SyncOffsetPagination[DocumentListResponse], document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Avido) -> None:
        response = client.documents.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(SyncOffsetPagination[DocumentListResponse], document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Avido) -> None:
        with client.documents.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(SyncOffsetPagination[DocumentListResponse], document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_chunks(self, client: Avido) -> None:
        document = client.documents.list_chunks()
        assert_matches_type(SyncOffsetPagination[DocumentChunk], document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_chunks_with_all_params(self, client: Avido) -> None:
        document = client.documents.list_chunks(
            document_id="123e4567-e89b-12d3-a456-426614174000",
            limit=25,
            order_by="createdAt",
            order_dir="desc",
            skip=0,
            status="APPROVED",
            version_id="321e4567-e89b-12d3-a456-426614174001",
        )
        assert_matches_type(SyncOffsetPagination[DocumentChunk], document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list_chunks(self, client: Avido) -> None:
        response = client.documents.with_raw_response.list_chunks()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(SyncOffsetPagination[DocumentChunk], document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list_chunks(self, client: Avido) -> None:
        with client.documents.with_streaming_response.list_chunks() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(SyncOffsetPagination[DocumentChunk], document, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDocuments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncAvido) -> None:
        document = await async_client.documents.create(
            assignee="user_123456789",
            content="This document describes the API endpoints...",
            title="API Documentation",
        )
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAvido) -> None:
        document = await async_client.documents.create(
            assignee="user_123456789",
            content="This document describes the API endpoints...",
            title="API Documentation",
            language="english",
            metadata={"foo": "bar"},
            original_sentences=["This is the first sentence.", "This is the second sentence."],
            scrape_job_id="321e4567-e89b-12d3-a456-426614174000",
            status="DRAFT",
        )
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAvido) -> None:
        response = await async_client.documents.with_raw_response.create(
            assignee="user_123456789",
            content="This document describes the API endpoints...",
            title="API Documentation",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAvido) -> None:
        async with async_client.documents.with_streaming_response.create(
            assignee="user_123456789",
            content="This document describes the API endpoints...",
            title="API Documentation",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(DocumentResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAvido) -> None:
        document = await async_client.documents.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAvido) -> None:
        response = await async_client.documents.with_raw_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAvido) -> None:
        async with async_client.documents.with_streaming_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(DocumentResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAvido) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.documents.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncAvido) -> None:
        document = await async_client.documents.list()
        assert_matches_type(AsyncOffsetPagination[DocumentListResponse], document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAvido) -> None:
        document = await async_client.documents.list(
            assignee="user_123456789",
            end_date=parse_datetime("2024-12-31T23:59:59.999Z"),
            limit=25,
            order_by="createdAt",
            order_dir="desc",
            scrape_job_id="321e4567-e89b-12d3-a456-426614174000",
            search="API documentation",
            skip=0,
            start_date=parse_datetime("2024-01-01T00:00:00.000Z"),
            status="APPROVED",
            tag_id=["string"],
        )
        assert_matches_type(AsyncOffsetPagination[DocumentListResponse], document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAvido) -> None:
        response = await async_client.documents.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(AsyncOffsetPagination[DocumentListResponse], document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAvido) -> None:
        async with async_client.documents.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(AsyncOffsetPagination[DocumentListResponse], document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_chunks(self, async_client: AsyncAvido) -> None:
        document = await async_client.documents.list_chunks()
        assert_matches_type(AsyncOffsetPagination[DocumentChunk], document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_chunks_with_all_params(self, async_client: AsyncAvido) -> None:
        document = await async_client.documents.list_chunks(
            document_id="123e4567-e89b-12d3-a456-426614174000",
            limit=25,
            order_by="createdAt",
            order_dir="desc",
            skip=0,
            status="APPROVED",
            version_id="321e4567-e89b-12d3-a456-426614174001",
        )
        assert_matches_type(AsyncOffsetPagination[DocumentChunk], document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list_chunks(self, async_client: AsyncAvido) -> None:
        response = await async_client.documents.with_raw_response.list_chunks()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(AsyncOffsetPagination[DocumentChunk], document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list_chunks(self, async_client: AsyncAvido) -> None:
        async with async_client.documents.with_streaming_response.list_chunks() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(AsyncOffsetPagination[DocumentChunk], document, path=["response"])

        assert cast(Any, response.is_closed) is True
