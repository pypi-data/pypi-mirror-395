# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "IngestCreateParams",
    "Event",
    "EventIngestTrace",
    "EventIngestTraceStep",
    "EventIngestTraceStepLlmStartStep",
    "EventIngestTraceStepLlmEndStep",
    "EventIngestTraceStepLlmEndStepUsage",
    "EventIngestTraceStepToolStep",
    "EventIngestTraceStepRetrieverStep",
    "EventIngestTraceStepLogStep",
    "EventIngestTraceStepGroupStep",
    "EventIngestTraceStepResponseStep",
    "EventIngestLlmStartStep",
    "EventIngestLlmEndStep",
    "EventIngestLlmEndStepUsage",
    "EventIngestToolStep",
    "EventIngestRetrieverStep",
    "EventIngestLogStep",
    "EventIngestGroupStep",
    "EventIngestResponseStep",
]


class IngestCreateParams(TypedDict, total=False):
    events: Required[Iterable[Event]]
    """Array of events to be ingested, which can be threads or traces."""


class EventIngestTraceStepLlmStartStep(TypedDict, total=False):
    id: Required[str]
    """UUID for the step."""

    event: Required[Literal["start"]]

    input: Required[str]
    """JSON input for this LLM trace event (e.g., the prompt)."""

    model_id: Required[Annotated[str, PropertyInfo(alias="modelId")]]
    """Model ID or name used for the LLM call."""

    timestamp: Required[str]
    """
    ISO-8601 datetime with up to microsecond precision (e.g.,
    2025-01-05T12:34:56.789123Z). Numeric millisecond timestamps (number or numeric
    string) are also accepted and automatically converted.
    """

    trace_id: Required[Annotated[str, PropertyInfo(alias="traceId")]]
    """UUID referencing the parent trace's ID."""

    type: Required[Literal["llm"]]

    group: str
    """Optionally, the key for a group step to group the step with."""

    metadata: Union[Dict[str, object], Iterable[object]]
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible, otherwise wrapped in { raw: val }.
    """

    name: str
    """The name of the step."""

    params: Union[Dict[str, object], Iterable[object]]
    """Arbitrary params for the step."""


class EventIngestTraceStepLlmEndStepUsage(TypedDict, total=False):
    completion_tokens: Required[Annotated[int, PropertyInfo(alias="completionTokens")]]
    """Number of completion tokens used by the LLM."""

    prompt_tokens: Required[Annotated[int, PropertyInfo(alias="promptTokens")]]
    """Number of prompt tokens used by the LLM."""


class EventIngestTraceStepLlmEndStep(TypedDict, total=False):
    id: Required[str]
    """UUID for the step."""

    event: Required[Literal["end"]]

    model_id: Required[Annotated[str, PropertyInfo(alias="modelId")]]
    """Model ID or name used for the LLM call."""

    timestamp: Required[str]
    """
    ISO-8601 datetime with up to microsecond precision (e.g.,
    2025-01-05T12:34:56.789123Z). Numeric millisecond timestamps (number or numeric
    string) are also accepted and automatically converted.
    """

    trace_id: Required[Annotated[str, PropertyInfo(alias="traceId")]]
    """UUID referencing the parent trace's ID."""

    type: Required[Literal["llm"]]

    group: str
    """Optionally, the key for a group step to group the step with."""

    metadata: Union[Dict[str, object], Iterable[object]]
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible, otherwise wrapped in { raw: val }.
    """

    name: str
    """The name of the step."""

    output: str
    """JSON describing the output.

    String inputs are parsed or wrapped in { message: val }.
    """

    params: Union[Dict[str, object], Iterable[object]]
    """Arbitrary params for the step."""

    usage: EventIngestTraceStepLlmEndStepUsage
    """Number of input and output tokens used by the LLM."""


class EventIngestTraceStepToolStep(TypedDict, total=False):
    id: Required[str]
    """UUID for the step."""

    timestamp: Required[str]
    """
    ISO-8601 datetime with up to microsecond precision (e.g.,
    2025-01-05T12:34:56.789123Z). Numeric millisecond timestamps (number or numeric
    string) are also accepted and automatically converted.
    """

    trace_id: Required[Annotated[str, PropertyInfo(alias="traceId")]]
    """UUID referencing the parent trace's ID."""

    type: Required[Literal["tool"]]

    group: str
    """Optionally, the key for a group step to group the step with."""

    metadata: Union[Dict[str, object], Iterable[object]]
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible, otherwise wrapped in { raw: val }.
    """

    name: str
    """The name of the step."""

    params: Union[Dict[str, object], Iterable[object]]
    """Arbitrary params for the step."""

    tool_input: Annotated[str, PropertyInfo(alias="toolInput")]
    """JSON input for the tool call."""

    tool_output: Annotated[str, PropertyInfo(alias="toolOutput")]
    """JSON output from the tool call."""


class EventIngestTraceStepRetrieverStep(TypedDict, total=False):
    id: Required[str]
    """UUID for the step."""

    query: Required[str]
    """Query used for RAG."""

    result: Required[str]
    """Retrieved text"""

    timestamp: Required[str]
    """
    ISO-8601 datetime with up to microsecond precision (e.g.,
    2025-01-05T12:34:56.789123Z). Numeric millisecond timestamps (number or numeric
    string) are also accepted and automatically converted.
    """

    trace_id: Required[Annotated[str, PropertyInfo(alias="traceId")]]
    """UUID referencing the parent trace's ID."""

    type: Required[Literal["retriever"]]

    group: str
    """Optionally, the key for a group step to group the step with."""

    metadata: Union[Dict[str, object], Iterable[object]]
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible, otherwise wrapped in { raw: val }.
    """

    name: str
    """The name of the step."""

    params: Union[Dict[str, object], Iterable[object]]
    """Arbitrary params for the step."""


class EventIngestTraceStepLogStep(TypedDict, total=False):
    id: Required[str]
    """UUID for the step."""

    content: Required[str]
    """The actual log message for this trace."""

    timestamp: Required[str]
    """
    ISO-8601 datetime with up to microsecond precision (e.g.,
    2025-01-05T12:34:56.789123Z). Numeric millisecond timestamps (number or numeric
    string) are also accepted and automatically converted.
    """

    trace_id: Required[Annotated[str, PropertyInfo(alias="traceId")]]
    """UUID referencing the parent trace's ID."""

    type: Required[Literal["log"]]

    group: str
    """Optionally, the key for a group step to group the step with."""

    metadata: Union[Dict[str, object], Iterable[object]]
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible, otherwise wrapped in { raw: val }.
    """

    name: str
    """The name of the step."""

    params: Union[Dict[str, object], Iterable[object]]
    """Arbitrary params for the step."""


class EventIngestTraceStepGroupStep(TypedDict, total=False):
    id: Required[str]
    """UUID for the step."""

    key: Required[str]
    """
    A unique identifier for the grouping, which must be appended to the
    corresponding steps
    """

    timestamp: Required[str]
    """
    ISO-8601 datetime with up to microsecond precision (e.g.,
    2025-01-05T12:34:56.789123Z). Numeric millisecond timestamps (number or numeric
    string) are also accepted and automatically converted.
    """

    trace_id: Required[Annotated[str, PropertyInfo(alias="traceId")]]
    """UUID referencing the parent trace's ID."""

    type: Required[Literal["group"]]

    group: str
    """Optionally, the key for a group step to group the step with."""

    metadata: Union[Dict[str, object], Iterable[object]]
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible, otherwise wrapped in { raw: val }.
    """

    name: str
    """The name of the step."""

    params: Union[Dict[str, object], Iterable[object]]
    """Arbitrary params for the step."""


class EventIngestTraceStepResponseStep(TypedDict, total=False):
    id: Required[str]
    """UUID for the step."""

    content: Required[str]
    """The response content from the AI to the user."""

    timestamp: Required[str]
    """
    ISO-8601 datetime with up to microsecond precision (e.g.,
    2025-01-05T12:34:56.789123Z). Numeric millisecond timestamps (number or numeric
    string) are also accepted and automatically converted.
    """

    trace_id: Required[Annotated[str, PropertyInfo(alias="traceId")]]
    """UUID referencing the parent trace's ID."""

    type: Required[Literal["response"]]

    group: str
    """Optionally, the key for a group step to group the step with."""

    metadata: Union[Dict[str, object], Iterable[object]]
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible, otherwise wrapped in { raw: val }.
    """

    name: str
    """The name of the step."""

    params: Union[Dict[str, object], Iterable[object]]
    """Arbitrary params for the step."""


EventIngestTraceStep: TypeAlias = Union[
    EventIngestTraceStepLlmStartStep,
    EventIngestTraceStepLlmEndStep,
    EventIngestTraceStepToolStep,
    EventIngestTraceStepRetrieverStep,
    EventIngestTraceStepLogStep,
    EventIngestTraceStepGroupStep,
    EventIngestTraceStepResponseStep,
]


class EventIngestTrace(TypedDict, total=False):
    timestamp: Required[str]
    """
    ISO-8601 datetime with up to microsecond precision (e.g.,
    2025-01-05T12:34:56.789123Z). Numeric millisecond timestamps (number or numeric
    string) are also accepted and automatically converted.
    """

    type: Required[Literal["trace"]]

    metadata: Union[str, Dict[str, object], Iterable[object]]
    """Arbitrary metadata for this thread (e.g., userId, source, etc.)."""

    reference_id: Annotated[str, PropertyInfo(alias="referenceId")]
    """
    An optional reference ID to link the trace to an existing conversation or
    interaction in your own database.
    """

    steps: Iterable[EventIngestTraceStep]
    """The steps associated with the trace."""

    test_id: Annotated[str, PropertyInfo(alias="testId")]
    """The associated Test if this was triggered by an Avido eval"""


class EventIngestLlmStartStep(TypedDict, total=False):
    event: Required[Literal["start"]]

    input: Required[Union[str, Dict[str, object], Iterable[object]]]
    """The input for the LLM step."""

    model_id: Required[Annotated[str, PropertyInfo(alias="modelId")]]
    """Model ID or name used for the LLM call."""

    timestamp: Required[str]
    """
    ISO-8601 datetime with up to microsecond precision (e.g.,
    2025-01-05T12:34:56.789123Z). Numeric millisecond timestamps (number or numeric
    string) are also accepted and automatically converted.
    """

    type: Required[Literal["llm"]]

    group: str
    """Optionally, the key for a group step to group the step with."""

    metadata: Union[Dict[str, object], Iterable[object]]
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible, otherwise wrapped in { raw: val }.
    """

    name: str
    """The name of the step."""

    params: Union[Dict[str, object], Iterable[object]]
    """Arbitrary params for the step."""

    trace_id: Annotated[str, PropertyInfo(alias="traceId")]
    """The trace ID (UUID)."""


class EventIngestLlmEndStepUsage(TypedDict, total=False):
    completion_tokens: Required[Annotated[int, PropertyInfo(alias="completionTokens")]]
    """Number of completion tokens used by the LLM."""

    prompt_tokens: Required[Annotated[int, PropertyInfo(alias="promptTokens")]]
    """Number of prompt tokens used by the LLM."""


class EventIngestLlmEndStep(TypedDict, total=False):
    event: Required[Literal["end"]]

    model_id: Required[Annotated[str, PropertyInfo(alias="modelId")]]
    """Model ID or name used for the LLM call."""

    timestamp: Required[str]
    """
    ISO-8601 datetime with up to microsecond precision (e.g.,
    2025-01-05T12:34:56.789123Z). Numeric millisecond timestamps (number or numeric
    string) are also accepted and automatically converted.
    """

    type: Required[Literal["llm"]]

    group: str
    """Optionally, the key for a group step to group the step with."""

    metadata: Union[Dict[str, object], Iterable[object]]
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible, otherwise wrapped in { raw: val }.
    """

    name: str
    """The name of the step."""

    output: Union[str, Dict[str, object], Iterable[object]]
    """The output for the LLM step."""

    params: Union[Dict[str, object], Iterable[object]]
    """Arbitrary params for the step."""

    trace_id: Annotated[str, PropertyInfo(alias="traceId")]
    """The trace ID (UUID)."""

    usage: EventIngestLlmEndStepUsage
    """Number of input and output tokens used by the LLM."""


class EventIngestToolStep(TypedDict, total=False):
    timestamp: Required[str]
    """
    ISO-8601 datetime with up to microsecond precision (e.g.,
    2025-01-05T12:34:56.789123Z). Numeric millisecond timestamps (number or numeric
    string) are also accepted and automatically converted.
    """

    type: Required[Literal["tool"]]

    group: str
    """Optionally, the key for a group step to group the step with."""

    metadata: Union[Dict[str, object], Iterable[object]]
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible, otherwise wrapped in { raw: val }.
    """

    name: str
    """The name of the step."""

    params: Union[Dict[str, object], Iterable[object]]
    """Arbitrary params for the step."""

    tool_input: Annotated[Union[str, Dict[str, object], Iterable[object]], PropertyInfo(alias="toolInput")]
    """The input for the tool step."""

    tool_output: Annotated[Union[str, Dict[str, object], Iterable[object]], PropertyInfo(alias="toolOutput")]
    """The output for the tool step."""

    trace_id: Annotated[str, PropertyInfo(alias="traceId")]
    """The trace ID (UUID)."""


class EventIngestRetrieverStep(TypedDict, total=False):
    query: Required[Union[str, Dict[str, object], Iterable[object]]]
    """The query for the retriever step."""

    result: Required[Union[str, Dict[str, object], Iterable[object]]]
    """The result for the retriever step."""

    timestamp: Required[str]
    """
    ISO-8601 datetime with up to microsecond precision (e.g.,
    2025-01-05T12:34:56.789123Z). Numeric millisecond timestamps (number or numeric
    string) are also accepted and automatically converted.
    """

    type: Required[Literal["retriever"]]

    group: str
    """Optionally, the key for a group step to group the step with."""

    metadata: Union[Dict[str, object], Iterable[object]]
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible, otherwise wrapped in { raw: val }.
    """

    name: str
    """The name of the step."""

    params: Union[str, Dict[str, object], Iterable[object]]
    """Arbitrary params for the step."""

    trace_id: Annotated[str, PropertyInfo(alias="traceId")]
    """The trace ID (UUID)."""


class EventIngestLogStep(TypedDict, total=False):
    content: Required[str]
    """The actual log message for this trace."""

    timestamp: Required[str]
    """
    ISO-8601 datetime with up to microsecond precision (e.g.,
    2025-01-05T12:34:56.789123Z). Numeric millisecond timestamps (number or numeric
    string) are also accepted and automatically converted.
    """

    type: Required[Literal["log"]]

    group: str
    """Optionally, the key for a group step to group the step with."""

    metadata: Union[Dict[str, object], Iterable[object]]
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible, otherwise wrapped in { raw: val }.
    """

    name: str
    """The name of the step."""

    params: Union[Dict[str, object], Iterable[object]]
    """Arbitrary params for the step."""

    trace_id: Annotated[str, PropertyInfo(alias="traceId")]
    """The trace ID (UUID)."""


class EventIngestGroupStep(TypedDict, total=False):
    key: Required[str]
    """
    A unique identifier for the grouping, which must be appended to the
    corresponding steps
    """

    timestamp: Required[str]
    """
    ISO-8601 datetime with up to microsecond precision (e.g.,
    2025-01-05T12:34:56.789123Z). Numeric millisecond timestamps (number or numeric
    string) are also accepted and automatically converted.
    """

    type: Required[Literal["group"]]

    group: str
    """Optionally, the key for a group step to group the step with."""

    metadata: Union[Dict[str, object], Iterable[object]]
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible, otherwise wrapped in { raw: val }.
    """

    name: str
    """The name of the step."""

    params: Union[Dict[str, object], Iterable[object]]
    """Arbitrary params for the step."""

    trace_id: Annotated[str, PropertyInfo(alias="traceId")]
    """The trace ID (UUID)."""


class EventIngestResponseStep(TypedDict, total=False):
    content: Required[Union[str, Dict[str, object], Iterable[object]]]
    """The response content from the AI to the user."""

    timestamp: Required[str]
    """
    ISO-8601 datetime with up to microsecond precision (e.g.,
    2025-01-05T12:34:56.789123Z). Numeric millisecond timestamps (number or numeric
    string) are also accepted and automatically converted.
    """

    type: Required[Literal["response"]]

    group: str
    """Optionally, the key for a group step to group the step with."""

    metadata: Union[Dict[str, object], Iterable[object]]
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible, otherwise wrapped in { raw: val }.
    """

    name: str
    """The name of the step."""

    params: Union[Dict[str, object], Iterable[object]]
    """Arbitrary params for the step."""

    trace_id: Annotated[str, PropertyInfo(alias="traceId")]
    """The trace ID (UUID)."""


Event: TypeAlias = Union[
    EventIngestTrace,
    EventIngestLlmStartStep,
    EventIngestLlmEndStep,
    EventIngestToolStep,
    EventIngestRetrieverStep,
    EventIngestLogStep,
    EventIngestGroupStep,
    EventIngestResponseStep,
]
