# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal

import httpx

from ..types import style_guide_list_params, style_guide_create_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncOffsetPagination, AsyncOffsetPagination
from .._base_client import AsyncPaginator, make_request_options
from ..types.style_guide import StyleGuide
from ..types.style_guide_response import StyleGuideResponse

__all__ = ["StyleGuidesResource", "AsyncStyleGuidesResource"]


class StyleGuidesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> StyleGuidesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Avido-AI/avido-py#accessing-raw-response-data-eg-headers
        """
        return StyleGuidesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> StyleGuidesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Avido-AI/avido-py#with_streaming_response
        """
        return StyleGuidesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        content: Iterable[style_guide_create_params.Content],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StyleGuideResponse:
        """
        Creates a new style guide.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v0/style-guides",
            body=maybe_transform({"content": content}, style_guide_create_params.StyleGuideCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StyleGuideResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StyleGuideResponse:
        """
        Retrieves detailed information about a specific style guide.

        Args:
          id: The unique identifier of the style guide

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v0/style-guides/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StyleGuideResponse,
        )

    def list(
        self,
        *,
        application_slug: str | Omit = omit,
        limit: int | Omit = omit,
        order_by: str | Omit = omit,
        order_dir: Literal["asc", "desc"] | Omit = omit,
        skip: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncOffsetPagination[StyleGuide]:
        """
        Retrieves a paginated list of style guides with optional filtering.

        Args:
          application_slug: Filter style guides by application slug

          limit: Number of items to include in the result set.

          order_by: Field to order by in the result set.

          order_dir: Order direction.

          skip: Number of items to skip before starting to collect the result set.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v0/style-guides",
            page=SyncOffsetPagination[StyleGuide],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "application_slug": application_slug,
                        "limit": limit,
                        "order_by": order_by,
                        "order_dir": order_dir,
                        "skip": skip,
                    },
                    style_guide_list_params.StyleGuideListParams,
                ),
            ),
            model=StyleGuide,
        )


class AsyncStyleGuidesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncStyleGuidesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Avido-AI/avido-py#accessing-raw-response-data-eg-headers
        """
        return AsyncStyleGuidesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncStyleGuidesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Avido-AI/avido-py#with_streaming_response
        """
        return AsyncStyleGuidesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        content: Iterable[style_guide_create_params.Content],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StyleGuideResponse:
        """
        Creates a new style guide.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v0/style-guides",
            body=await async_maybe_transform({"content": content}, style_guide_create_params.StyleGuideCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StyleGuideResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StyleGuideResponse:
        """
        Retrieves detailed information about a specific style guide.

        Args:
          id: The unique identifier of the style guide

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v0/style-guides/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StyleGuideResponse,
        )

    def list(
        self,
        *,
        application_slug: str | Omit = omit,
        limit: int | Omit = omit,
        order_by: str | Omit = omit,
        order_dir: Literal["asc", "desc"] | Omit = omit,
        skip: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[StyleGuide, AsyncOffsetPagination[StyleGuide]]:
        """
        Retrieves a paginated list of style guides with optional filtering.

        Args:
          application_slug: Filter style guides by application slug

          limit: Number of items to include in the result set.

          order_by: Field to order by in the result set.

          order_dir: Order direction.

          skip: Number of items to skip before starting to collect the result set.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v0/style-guides",
            page=AsyncOffsetPagination[StyleGuide],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "application_slug": application_slug,
                        "limit": limit,
                        "order_by": order_by,
                        "order_dir": order_dir,
                        "skip": skip,
                    },
                    style_guide_list_params.StyleGuideListParams,
                ),
            ),
            model=StyleGuide,
        )


class StyleGuidesResourceWithRawResponse:
    def __init__(self, style_guides: StyleGuidesResource) -> None:
        self._style_guides = style_guides

        self.create = to_raw_response_wrapper(
            style_guides.create,
        )
        self.retrieve = to_raw_response_wrapper(
            style_guides.retrieve,
        )
        self.list = to_raw_response_wrapper(
            style_guides.list,
        )


class AsyncStyleGuidesResourceWithRawResponse:
    def __init__(self, style_guides: AsyncStyleGuidesResource) -> None:
        self._style_guides = style_guides

        self.create = async_to_raw_response_wrapper(
            style_guides.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            style_guides.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            style_guides.list,
        )


class StyleGuidesResourceWithStreamingResponse:
    def __init__(self, style_guides: StyleGuidesResource) -> None:
        self._style_guides = style_guides

        self.create = to_streamed_response_wrapper(
            style_guides.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            style_guides.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            style_guides.list,
        )


class AsyncStyleGuidesResourceWithStreamingResponse:
    def __init__(self, style_guides: AsyncStyleGuidesResource) -> None:
        self._style_guides = style_guides

        self.create = async_to_streamed_response_wrapper(
            style_guides.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            style_guides.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            style_guides.list,
        )
