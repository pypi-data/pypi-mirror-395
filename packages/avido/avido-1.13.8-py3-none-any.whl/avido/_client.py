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
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from .resources import (
    runs,
    tasks,
    tests,
    ingest,
    topics,
    traces,
    documents,
    annotations,
    applications,
    style_guides,
    validate_webhook,
)
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import AvidoError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Avido", "AsyncAvido", "Client", "AsyncClient"]


class Avido(SyncAPIClient):
    validate_webhook: validate_webhook.ValidateWebhookResource
    applications: applications.ApplicationsResource
    traces: traces.TracesResource
    ingest: ingest.IngestResource
    tasks: tasks.TasksResource
    tests: tests.TestsResource
    topics: topics.TopicsResource
    annotations: annotations.AnnotationsResource
    runs: runs.RunsResource
    style_guides: style_guides.StyleGuidesResource
    documents: documents.DocumentsResource
    with_raw_response: AvidoWithRawResponse
    with_streaming_response: AvidoWithStreamedResponse

    # client options
    api_key: str
    application_id: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        application_id: str | None = None,
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
        """Construct a new synchronous Avido client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `AVIDO_API_KEY`
        - `application_id` from `AVIDO_APPLICATION_ID`
        """
        if api_key is None:
            api_key = os.environ.get("AVIDO_API_KEY")
        if api_key is None:
            raise AvidoError(
                "The api_key client option must be set either by passing api_key to the client or by setting the AVIDO_API_KEY environment variable"
            )
        self.api_key = api_key

        if application_id is None:
            application_id = os.environ.get("AVIDO_APPLICATION_ID")
        if application_id is None:
            raise AvidoError(
                "The application_id client option must be set either by passing application_id to the client or by setting the AVIDO_APPLICATION_ID environment variable"
            )
        self.application_id = application_id

        if base_url is None:
            base_url = os.environ.get("AVIDO_BASE_URL")
        if base_url is None:
            base_url = f"https://api.avidoai.com"

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

        self.validate_webhook = validate_webhook.ValidateWebhookResource(self)
        self.applications = applications.ApplicationsResource(self)
        self.traces = traces.TracesResource(self)
        self.ingest = ingest.IngestResource(self)
        self.tasks = tasks.TasksResource(self)
        self.tests = tests.TestsResource(self)
        self.topics = topics.TopicsResource(self)
        self.annotations = annotations.AnnotationsResource(self)
        self.runs = runs.RunsResource(self)
        self.style_guides = style_guides.StyleGuidesResource(self)
        self.documents = documents.DocumentsResource(self)
        self.with_raw_response = AvidoWithRawResponse(self)
        self.with_streaming_response = AvidoWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"x-api-key": api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            "x-application-id": self.application_id,
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        application_id: str | None = None,
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
            api_key=api_key or self.api_key,
            application_id=application_id or self.application_id,
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


class AsyncAvido(AsyncAPIClient):
    validate_webhook: validate_webhook.AsyncValidateWebhookResource
    applications: applications.AsyncApplicationsResource
    traces: traces.AsyncTracesResource
    ingest: ingest.AsyncIngestResource
    tasks: tasks.AsyncTasksResource
    tests: tests.AsyncTestsResource
    topics: topics.AsyncTopicsResource
    annotations: annotations.AsyncAnnotationsResource
    runs: runs.AsyncRunsResource
    style_guides: style_guides.AsyncStyleGuidesResource
    documents: documents.AsyncDocumentsResource
    with_raw_response: AsyncAvidoWithRawResponse
    with_streaming_response: AsyncAvidoWithStreamedResponse

    # client options
    api_key: str
    application_id: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        application_id: str | None = None,
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
        """Construct a new async AsyncAvido client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `AVIDO_API_KEY`
        - `application_id` from `AVIDO_APPLICATION_ID`
        """
        if api_key is None:
            api_key = os.environ.get("AVIDO_API_KEY")
        if api_key is None:
            raise AvidoError(
                "The api_key client option must be set either by passing api_key to the client or by setting the AVIDO_API_KEY environment variable"
            )
        self.api_key = api_key

        if application_id is None:
            application_id = os.environ.get("AVIDO_APPLICATION_ID")
        if application_id is None:
            raise AvidoError(
                "The application_id client option must be set either by passing application_id to the client or by setting the AVIDO_APPLICATION_ID environment variable"
            )
        self.application_id = application_id

        if base_url is None:
            base_url = os.environ.get("AVIDO_BASE_URL")
        if base_url is None:
            base_url = f"https://api.avidoai.com"

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

        self.validate_webhook = validate_webhook.AsyncValidateWebhookResource(self)
        self.applications = applications.AsyncApplicationsResource(self)
        self.traces = traces.AsyncTracesResource(self)
        self.ingest = ingest.AsyncIngestResource(self)
        self.tasks = tasks.AsyncTasksResource(self)
        self.tests = tests.AsyncTestsResource(self)
        self.topics = topics.AsyncTopicsResource(self)
        self.annotations = annotations.AsyncAnnotationsResource(self)
        self.runs = runs.AsyncRunsResource(self)
        self.style_guides = style_guides.AsyncStyleGuidesResource(self)
        self.documents = documents.AsyncDocumentsResource(self)
        self.with_raw_response = AsyncAvidoWithRawResponse(self)
        self.with_streaming_response = AsyncAvidoWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"x-api-key": api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            "x-application-id": self.application_id,
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        application_id: str | None = None,
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
            api_key=api_key or self.api_key,
            application_id=application_id or self.application_id,
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


class AvidoWithRawResponse:
    def __init__(self, client: Avido) -> None:
        self.validate_webhook = validate_webhook.ValidateWebhookResourceWithRawResponse(client.validate_webhook)
        self.applications = applications.ApplicationsResourceWithRawResponse(client.applications)
        self.traces = traces.TracesResourceWithRawResponse(client.traces)
        self.ingest = ingest.IngestResourceWithRawResponse(client.ingest)
        self.tasks = tasks.TasksResourceWithRawResponse(client.tasks)
        self.tests = tests.TestsResourceWithRawResponse(client.tests)
        self.topics = topics.TopicsResourceWithRawResponse(client.topics)
        self.annotations = annotations.AnnotationsResourceWithRawResponse(client.annotations)
        self.runs = runs.RunsResourceWithRawResponse(client.runs)
        self.style_guides = style_guides.StyleGuidesResourceWithRawResponse(client.style_guides)
        self.documents = documents.DocumentsResourceWithRawResponse(client.documents)


class AsyncAvidoWithRawResponse:
    def __init__(self, client: AsyncAvido) -> None:
        self.validate_webhook = validate_webhook.AsyncValidateWebhookResourceWithRawResponse(client.validate_webhook)
        self.applications = applications.AsyncApplicationsResourceWithRawResponse(client.applications)
        self.traces = traces.AsyncTracesResourceWithRawResponse(client.traces)
        self.ingest = ingest.AsyncIngestResourceWithRawResponse(client.ingest)
        self.tasks = tasks.AsyncTasksResourceWithRawResponse(client.tasks)
        self.tests = tests.AsyncTestsResourceWithRawResponse(client.tests)
        self.topics = topics.AsyncTopicsResourceWithRawResponse(client.topics)
        self.annotations = annotations.AsyncAnnotationsResourceWithRawResponse(client.annotations)
        self.runs = runs.AsyncRunsResourceWithRawResponse(client.runs)
        self.style_guides = style_guides.AsyncStyleGuidesResourceWithRawResponse(client.style_guides)
        self.documents = documents.AsyncDocumentsResourceWithRawResponse(client.documents)


class AvidoWithStreamedResponse:
    def __init__(self, client: Avido) -> None:
        self.validate_webhook = validate_webhook.ValidateWebhookResourceWithStreamingResponse(client.validate_webhook)
        self.applications = applications.ApplicationsResourceWithStreamingResponse(client.applications)
        self.traces = traces.TracesResourceWithStreamingResponse(client.traces)
        self.ingest = ingest.IngestResourceWithStreamingResponse(client.ingest)
        self.tasks = tasks.TasksResourceWithStreamingResponse(client.tasks)
        self.tests = tests.TestsResourceWithStreamingResponse(client.tests)
        self.topics = topics.TopicsResourceWithStreamingResponse(client.topics)
        self.annotations = annotations.AnnotationsResourceWithStreamingResponse(client.annotations)
        self.runs = runs.RunsResourceWithStreamingResponse(client.runs)
        self.style_guides = style_guides.StyleGuidesResourceWithStreamingResponse(client.style_guides)
        self.documents = documents.DocumentsResourceWithStreamingResponse(client.documents)


class AsyncAvidoWithStreamedResponse:
    def __init__(self, client: AsyncAvido) -> None:
        self.validate_webhook = validate_webhook.AsyncValidateWebhookResourceWithStreamingResponse(
            client.validate_webhook
        )
        self.applications = applications.AsyncApplicationsResourceWithStreamingResponse(client.applications)
        self.traces = traces.AsyncTracesResourceWithStreamingResponse(client.traces)
        self.ingest = ingest.AsyncIngestResourceWithStreamingResponse(client.ingest)
        self.tasks = tasks.AsyncTasksResourceWithStreamingResponse(client.tasks)
        self.tests = tests.AsyncTestsResourceWithStreamingResponse(client.tests)
        self.topics = topics.AsyncTopicsResourceWithStreamingResponse(client.topics)
        self.annotations = annotations.AsyncAnnotationsResourceWithStreamingResponse(client.annotations)
        self.runs = runs.AsyncRunsResourceWithStreamingResponse(client.runs)
        self.style_guides = style_guides.AsyncStyleGuidesResourceWithStreamingResponse(client.style_guides)
        self.documents = documents.AsyncDocumentsResourceWithStreamingResponse(client.documents)


Client = Avido

AsyncClient = AsyncAvido
