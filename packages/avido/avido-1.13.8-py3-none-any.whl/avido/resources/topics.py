# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal

import httpx

from ..types import topic_list_params, topic_create_params
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
from ..types.topic import Topic
from .._base_client import AsyncPaginator, make_request_options
from ..types.topic_response import TopicResponse

__all__ = ["TopicsResource", "AsyncTopicsResource"]


class TopicsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TopicsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Avido-AI/avido-py#accessing-raw-response-data-eg-headers
        """
        return TopicsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TopicsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Avido-AI/avido-py#with_streaming_response
        """
        return TopicsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        title: str,
        baseline: Optional[float] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TopicResponse:
        """
        Creates a new topic.

        Args:
          title: Title of the topic

          baseline: Optional baseline score for this topic

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v0/topics",
            body=maybe_transform(
                {
                    "title": title,
                    "baseline": baseline,
                },
                topic_create_params.TopicCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicResponse,
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
    ) -> TopicResponse:
        """
        Retrieves detailed information about a specific topic.

        Args:
          id: The unique identifier of the topic

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v0/topics/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicResponse,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        order_by: str | Omit = omit,
        order_dir: Literal["asc", "desc"] | Omit = omit,
        skip: int | Omit = omit,
        title: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncOffsetPagination[Topic]:
        """
        Retrieves a paginated list of topics with optional filtering.

        Args:
          limit: Number of items to include in the result set.

          order_by: Field to order by in the result set.

          order_dir: Order direction.

          skip: Number of items to skip before starting to collect the result set.

          title: Filter by topic title (case-insensitive)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v0/topics",
            page=SyncOffsetPagination[Topic],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "order_by": order_by,
                        "order_dir": order_dir,
                        "skip": skip,
                        "title": title,
                    },
                    topic_list_params.TopicListParams,
                ),
            ),
            model=Topic,
        )


class AsyncTopicsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTopicsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Avido-AI/avido-py#accessing-raw-response-data-eg-headers
        """
        return AsyncTopicsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTopicsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Avido-AI/avido-py#with_streaming_response
        """
        return AsyncTopicsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        title: str,
        baseline: Optional[float] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TopicResponse:
        """
        Creates a new topic.

        Args:
          title: Title of the topic

          baseline: Optional baseline score for this topic

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v0/topics",
            body=await async_maybe_transform(
                {
                    "title": title,
                    "baseline": baseline,
                },
                topic_create_params.TopicCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicResponse,
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
    ) -> TopicResponse:
        """
        Retrieves detailed information about a specific topic.

        Args:
          id: The unique identifier of the topic

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v0/topics/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicResponse,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        order_by: str | Omit = omit,
        order_dir: Literal["asc", "desc"] | Omit = omit,
        skip: int | Omit = omit,
        title: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Topic, AsyncOffsetPagination[Topic]]:
        """
        Retrieves a paginated list of topics with optional filtering.

        Args:
          limit: Number of items to include in the result set.

          order_by: Field to order by in the result set.

          order_dir: Order direction.

          skip: Number of items to skip before starting to collect the result set.

          title: Filter by topic title (case-insensitive)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v0/topics",
            page=AsyncOffsetPagination[Topic],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "order_by": order_by,
                        "order_dir": order_dir,
                        "skip": skip,
                        "title": title,
                    },
                    topic_list_params.TopicListParams,
                ),
            ),
            model=Topic,
        )


class TopicsResourceWithRawResponse:
    def __init__(self, topics: TopicsResource) -> None:
        self._topics = topics

        self.create = to_raw_response_wrapper(
            topics.create,
        )
        self.retrieve = to_raw_response_wrapper(
            topics.retrieve,
        )
        self.list = to_raw_response_wrapper(
            topics.list,
        )


class AsyncTopicsResourceWithRawResponse:
    def __init__(self, topics: AsyncTopicsResource) -> None:
        self._topics = topics

        self.create = async_to_raw_response_wrapper(
            topics.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            topics.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            topics.list,
        )


class TopicsResourceWithStreamingResponse:
    def __init__(self, topics: TopicsResource) -> None:
        self._topics = topics

        self.create = to_streamed_response_wrapper(
            topics.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            topics.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            topics.list,
        )


class AsyncTopicsResourceWithStreamingResponse:
    def __init__(self, topics: AsyncTopicsResource) -> None:
        self._topics = topics

        self.create = async_to_streamed_response_wrapper(
            topics.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            topics.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            topics.list,
        )
