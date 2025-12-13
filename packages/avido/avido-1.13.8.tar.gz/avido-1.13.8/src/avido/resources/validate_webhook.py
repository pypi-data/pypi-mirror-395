# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import validate_webhook_validate_params
from .._types import Body, Query, Headers, NotGiven, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.validate_webhook_validate_response import ValidateWebhookValidateResponse

__all__ = ["ValidateWebhookResource", "AsyncValidateWebhookResource"]


class ValidateWebhookResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ValidateWebhookResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Avido-AI/avido-py#accessing-raw-response-data-eg-headers
        """
        return ValidateWebhookResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ValidateWebhookResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Avido-AI/avido-py#with_streaming_response
        """
        return ValidateWebhookResourceWithStreamingResponse(self)

    def validate(
        self,
        *,
        body: validate_webhook_validate_params.Body,
        signature: str,
        timestamp: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ValidateWebhookValidateResponse:
        """
        Checks the body (including timestamp and signature) against the configured
        webhook secret. Returns `{ valid: true }` if the signature is valid.

        Args:
          body: Payload sent to the configured webhook whenever a task test is triggered.

          signature: HMAC signature for the request body.

          timestamp: Timestamp (in milliseconds) for the request.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v0/validate-webhook",
            body=maybe_transform(
                {
                    "body": body,
                    "signature": signature,
                    "timestamp": timestamp,
                },
                validate_webhook_validate_params.ValidateWebhookValidateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ValidateWebhookValidateResponse,
        )


class AsyncValidateWebhookResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncValidateWebhookResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Avido-AI/avido-py#accessing-raw-response-data-eg-headers
        """
        return AsyncValidateWebhookResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncValidateWebhookResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Avido-AI/avido-py#with_streaming_response
        """
        return AsyncValidateWebhookResourceWithStreamingResponse(self)

    async def validate(
        self,
        *,
        body: validate_webhook_validate_params.Body,
        signature: str,
        timestamp: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ValidateWebhookValidateResponse:
        """
        Checks the body (including timestamp and signature) against the configured
        webhook secret. Returns `{ valid: true }` if the signature is valid.

        Args:
          body: Payload sent to the configured webhook whenever a task test is triggered.

          signature: HMAC signature for the request body.

          timestamp: Timestamp (in milliseconds) for the request.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v0/validate-webhook",
            body=await async_maybe_transform(
                {
                    "body": body,
                    "signature": signature,
                    "timestamp": timestamp,
                },
                validate_webhook_validate_params.ValidateWebhookValidateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ValidateWebhookValidateResponse,
        )


class ValidateWebhookResourceWithRawResponse:
    def __init__(self, validate_webhook: ValidateWebhookResource) -> None:
        self._validate_webhook = validate_webhook

        self.validate = to_raw_response_wrapper(
            validate_webhook.validate,
        )


class AsyncValidateWebhookResourceWithRawResponse:
    def __init__(self, validate_webhook: AsyncValidateWebhookResource) -> None:
        self._validate_webhook = validate_webhook

        self.validate = async_to_raw_response_wrapper(
            validate_webhook.validate,
        )


class ValidateWebhookResourceWithStreamingResponse:
    def __init__(self, validate_webhook: ValidateWebhookResource) -> None:
        self._validate_webhook = validate_webhook

        self.validate = to_streamed_response_wrapper(
            validate_webhook.validate,
        )


class AsyncValidateWebhookResourceWithStreamingResponse:
    def __init__(self, validate_webhook: AsyncValidateWebhookResource) -> None:
        self._validate_webhook = validate_webhook

        self.validate = async_to_streamed_response_wrapper(
            validate_webhook.validate,
        )
