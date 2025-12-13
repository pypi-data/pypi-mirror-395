# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from avido import Avido, AsyncAvido
from avido.types import TestListResponse, TestRetrieveResponse
from tests.utils import assert_matches_type
from avido._utils import parse_datetime
from avido.pagination import SyncOffsetPagination, AsyncOffsetPagination

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTests:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Avido) -> None:
        test = client.tests.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(TestRetrieveResponse, test, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Avido) -> None:
        response = client.tests.with_raw_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test = response.parse()
        assert_matches_type(TestRetrieveResponse, test, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Avido) -> None:
        with client.tests.with_streaming_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test = response.parse()
            assert_matches_type(TestRetrieveResponse, test, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Avido) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.tests.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Avido) -> None:
        test = client.tests.list()
        assert_matches_type(SyncOffsetPagination[TestListResponse], test, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Avido) -> None:
        test = client.tests.list(
            end_date=parse_datetime("2024-12-31T23:59:59.999Z"),
            eval_definition_id=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            limit=25,
            order_by="createdAt",
            order_dir="desc",
            pass_rate_statuses=["success", "warning"],
            skip=0,
            start_date=parse_datetime("2024-01-01T00:00:00.000Z"),
            status=["COMPLETED", "FAILED"],
            task_id="456e4567-e89b-12d3-a456-426614174000",
            trace_id="789e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(SyncOffsetPagination[TestListResponse], test, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Avido) -> None:
        response = client.tests.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test = response.parse()
        assert_matches_type(SyncOffsetPagination[TestListResponse], test, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Avido) -> None:
        with client.tests.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test = response.parse()
            assert_matches_type(SyncOffsetPagination[TestListResponse], test, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTests:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAvido) -> None:
        test = await async_client.tests.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(TestRetrieveResponse, test, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAvido) -> None:
        response = await async_client.tests.with_raw_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test = await response.parse()
        assert_matches_type(TestRetrieveResponse, test, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAvido) -> None:
        async with async_client.tests.with_streaming_response.retrieve(
            "123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test = await response.parse()
            assert_matches_type(TestRetrieveResponse, test, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAvido) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.tests.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncAvido) -> None:
        test = await async_client.tests.list()
        assert_matches_type(AsyncOffsetPagination[TestListResponse], test, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAvido) -> None:
        test = await async_client.tests.list(
            end_date=parse_datetime("2024-12-31T23:59:59.999Z"),
            eval_definition_id=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            limit=25,
            order_by="createdAt",
            order_dir="desc",
            pass_rate_statuses=["success", "warning"],
            skip=0,
            start_date=parse_datetime("2024-01-01T00:00:00.000Z"),
            status=["COMPLETED", "FAILED"],
            task_id="456e4567-e89b-12d3-a456-426614174000",
            trace_id="789e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(AsyncOffsetPagination[TestListResponse], test, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAvido) -> None:
        response = await async_client.tests.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test = await response.parse()
        assert_matches_type(AsyncOffsetPagination[TestListResponse], test, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAvido) -> None:
        async with async_client.tests.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test = await response.parse()
            assert_matches_type(AsyncOffsetPagination[TestListResponse], test, path=["response"])

        assert cast(Any, response.is_closed) is True
