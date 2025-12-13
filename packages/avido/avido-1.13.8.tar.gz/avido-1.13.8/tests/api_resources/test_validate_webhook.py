# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from avido import Avido, AsyncAvido
from avido.types import ValidateWebhookValidateResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestValidateWebhook:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_validate(self, client: Avido) -> None:
        validate_webhook = client.validate_webhook.validate(
            body={
                "prompt": "I lost my card, please block it.",
                "test_id": "123e4567-e89b-12d3-a456-426614174000",
            },
            signature="abc123signature",
            timestamp=1687802842609,
        )
        assert_matches_type(ValidateWebhookValidateResponse, validate_webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_validate_with_all_params(self, client: Avido) -> None:
        validate_webhook = client.validate_webhook.validate(
            body={
                "prompt": "I lost my card, please block it.",
                "test_id": "123e4567-e89b-12d3-a456-426614174000",
                "experiment": {
                    "experiment_id": "123e4567-e89b-12d3-a456-426614174000",
                    "experiment_variant_id": "123e4567-e89b-12d3-a456-426614174000",
                    "overrides": {
                        "foo": {
                            "temperature": "bar",
                            "system": "bar",
                        }
                    },
                },
                "metadata": {
                    "customerId": "bar",
                    "priority": "bar",
                },
            },
            signature="abc123signature",
            timestamp=1687802842609,
        )
        assert_matches_type(ValidateWebhookValidateResponse, validate_webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_validate(self, client: Avido) -> None:
        response = client.validate_webhook.with_raw_response.validate(
            body={
                "prompt": "I lost my card, please block it.",
                "test_id": "123e4567-e89b-12d3-a456-426614174000",
            },
            signature="abc123signature",
            timestamp=1687802842609,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validate_webhook = response.parse()
        assert_matches_type(ValidateWebhookValidateResponse, validate_webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_validate(self, client: Avido) -> None:
        with client.validate_webhook.with_streaming_response.validate(
            body={
                "prompt": "I lost my card, please block it.",
                "test_id": "123e4567-e89b-12d3-a456-426614174000",
            },
            signature="abc123signature",
            timestamp=1687802842609,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validate_webhook = response.parse()
            assert_matches_type(ValidateWebhookValidateResponse, validate_webhook, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncValidateWebhook:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_validate(self, async_client: AsyncAvido) -> None:
        validate_webhook = await async_client.validate_webhook.validate(
            body={
                "prompt": "I lost my card, please block it.",
                "test_id": "123e4567-e89b-12d3-a456-426614174000",
            },
            signature="abc123signature",
            timestamp=1687802842609,
        )
        assert_matches_type(ValidateWebhookValidateResponse, validate_webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_validate_with_all_params(self, async_client: AsyncAvido) -> None:
        validate_webhook = await async_client.validate_webhook.validate(
            body={
                "prompt": "I lost my card, please block it.",
                "test_id": "123e4567-e89b-12d3-a456-426614174000",
                "experiment": {
                    "experiment_id": "123e4567-e89b-12d3-a456-426614174000",
                    "experiment_variant_id": "123e4567-e89b-12d3-a456-426614174000",
                    "overrides": {
                        "foo": {
                            "temperature": "bar",
                            "system": "bar",
                        }
                    },
                },
                "metadata": {
                    "customerId": "bar",
                    "priority": "bar",
                },
            },
            signature="abc123signature",
            timestamp=1687802842609,
        )
        assert_matches_type(ValidateWebhookValidateResponse, validate_webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_validate(self, async_client: AsyncAvido) -> None:
        response = await async_client.validate_webhook.with_raw_response.validate(
            body={
                "prompt": "I lost my card, please block it.",
                "test_id": "123e4567-e89b-12d3-a456-426614174000",
            },
            signature="abc123signature",
            timestamp=1687802842609,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validate_webhook = await response.parse()
        assert_matches_type(ValidateWebhookValidateResponse, validate_webhook, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_validate(self, async_client: AsyncAvido) -> None:
        async with async_client.validate_webhook.with_streaming_response.validate(
            body={
                "prompt": "I lost my card, please block it.",
                "test_id": "123e4567-e89b-12d3-a456-426614174000",
            },
            signature="abc123signature",
            timestamp=1687802842609,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validate_webhook = await response.parse()
            assert_matches_type(ValidateWebhookValidateResponse, validate_webhook, path=["response"])

        assert cast(Any, response.is_closed) is True
