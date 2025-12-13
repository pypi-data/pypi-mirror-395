# ValidateWebhook

Types:

```python
from avido.types import ValidateWebhookValidateResponse
```

Methods:

- <code title="post /v0/validate-webhook">client.validate_webhook.<a href="./src/avido/resources/validate_webhook.py">validate</a>(\*\*<a href="src/avido/types/validate_webhook_validate_params.py">params</a>) -> <a href="./src/avido/types/validate_webhook_validate_response.py">ValidateWebhookValidateResponse</a></code>

# Applications

Types:

```python
from avido.types import Application, ApplicationResponse
```

Methods:

- <code title="post /v0/applications">client.applications.<a href="./src/avido/resources/applications.py">create</a>(\*\*<a href="src/avido/types/application_create_params.py">params</a>) -> <a href="./src/avido/types/application_response.py">ApplicationResponse</a></code>
- <code title="get /v0/applications/{id}">client.applications.<a href="./src/avido/resources/applications.py">retrieve</a>(id) -> <a href="./src/avido/types/application_response.py">ApplicationResponse</a></code>
- <code title="get /v0/applications">client.applications.<a href="./src/avido/resources/applications.py">list</a>(\*\*<a href="src/avido/types/application_list_params.py">params</a>) -> <a href="./src/avido/types/application.py">SyncOffsetPagination[Application]</a></code>

# Traces

Types:

```python
from avido.types import Trace, TraceRetrieveResponse
```

Methods:

- <code title="get /v0/traces/{id}">client.traces.<a href="./src/avido/resources/traces.py">retrieve</a>(id) -> <a href="./src/avido/types/trace_retrieve_response.py">TraceRetrieveResponse</a></code>
- <code title="get /v0/traces">client.traces.<a href="./src/avido/resources/traces.py">list</a>(\*\*<a href="src/avido/types/trace_list_params.py">params</a>) -> <a href="./src/avido/types/trace.py">SyncOffsetPagination[Trace]</a></code>

# Ingest

Types:

```python
from avido.types import IngestCreateResponse
```

Methods:

- <code title="post /v0/ingest">client.ingest.<a href="./src/avido/resources/ingest.py">create</a>(\*\*<a href="src/avido/types/ingest_create_params.py">params</a>) -> <a href="./src/avido/types/ingest_create_response.py">IngestCreateResponse</a></code>

# Tasks

Types:

```python
from avido.types import Task, TaskResponse, TaskListResponse
```

Methods:

- <code title="post /v0/tasks">client.tasks.<a href="./src/avido/resources/tasks.py">create</a>(\*\*<a href="src/avido/types/task_create_params.py">params</a>) -> <a href="./src/avido/types/task_response.py">TaskResponse</a></code>
- <code title="get /v0/tasks/{id}">client.tasks.<a href="./src/avido/resources/tasks.py">retrieve</a>(id) -> <a href="./src/avido/types/task_response.py">TaskResponse</a></code>
- <code title="get /v0/tasks">client.tasks.<a href="./src/avido/resources/tasks.py">list</a>(\*\*<a href="src/avido/types/task_list_params.py">params</a>) -> <a href="./src/avido/types/task_list_response.py">SyncOffsetPagination[TaskListResponse]</a></code>
- <code title="post /v0/tasks/trigger">client.tasks.<a href="./src/avido/resources/tasks.py">trigger</a>(\*\*<a href="src/avido/types/task_trigger_params.py">params</a>) -> None</code>

# Evals

Types:

```python
from avido.types import Eval
```

# Tests

Types:

```python
from avido.types import Test, TestRetrieveResponse, TestListResponse
```

Methods:

- <code title="get /v0/tests/{id}">client.tests.<a href="./src/avido/resources/tests.py">retrieve</a>(id) -> <a href="./src/avido/types/test_retrieve_response.py">TestRetrieveResponse</a></code>
- <code title="get /v0/tests">client.tests.<a href="./src/avido/resources/tests.py">list</a>(\*\*<a href="src/avido/types/test_list_params.py">params</a>) -> <a href="./src/avido/types/test_list_response.py">SyncOffsetPagination[TestListResponse]</a></code>

# Topics

Types:

```python
from avido.types import Topic, TopicResponse
```

Methods:

- <code title="post /v0/topics">client.topics.<a href="./src/avido/resources/topics.py">create</a>(\*\*<a href="src/avido/types/topic_create_params.py">params</a>) -> <a href="./src/avido/types/topic_response.py">TopicResponse</a></code>
- <code title="get /v0/topics/{id}">client.topics.<a href="./src/avido/resources/topics.py">retrieve</a>(id) -> <a href="./src/avido/types/topic_response.py">TopicResponse</a></code>
- <code title="get /v0/topics">client.topics.<a href="./src/avido/resources/topics.py">list</a>(\*\*<a href="src/avido/types/topic_list_params.py">params</a>) -> <a href="./src/avido/types/topic.py">SyncOffsetPagination[Topic]</a></code>

# Annotations

Types:

```python
from avido.types import Annotation, AnnotationResponse
```

Methods:

- <code title="post /v0/annotations">client.annotations.<a href="./src/avido/resources/annotations.py">create</a>(\*\*<a href="src/avido/types/annotation_create_params.py">params</a>) -> <a href="./src/avido/types/annotation_response.py">AnnotationResponse</a></code>
- <code title="get /v0/annotations/{id}">client.annotations.<a href="./src/avido/resources/annotations.py">retrieve</a>(id) -> <a href="./src/avido/types/annotation_response.py">AnnotationResponse</a></code>
- <code title="get /v0/annotations">client.annotations.<a href="./src/avido/resources/annotations.py">list</a>(\*\*<a href="src/avido/types/annotation_list_params.py">params</a>) -> <a href="./src/avido/types/annotation.py">SyncOffsetPagination[Annotation]</a></code>

# Runs

Types:

```python
from avido.types import Run, RunRetrieveResponse
```

Methods:

- <code title="get /v0/runs/{id}">client.runs.<a href="./src/avido/resources/runs.py">retrieve</a>(id) -> <a href="./src/avido/types/run_retrieve_response.py">RunRetrieveResponse</a></code>
- <code title="get /v0/runs">client.runs.<a href="./src/avido/resources/runs.py">list</a>(\*\*<a href="src/avido/types/run_list_params.py">params</a>) -> <a href="./src/avido/types/run.py">SyncOffsetPagination[Run]</a></code>

# StyleGuides

Types:

```python
from avido.types import StyleGuide, StyleGuideResponse
```

Methods:

- <code title="post /v0/style-guides">client.style_guides.<a href="./src/avido/resources/style_guides.py">create</a>(\*\*<a href="src/avido/types/style_guide_create_params.py">params</a>) -> <a href="./src/avido/types/style_guide_response.py">StyleGuideResponse</a></code>
- <code title="get /v0/style-guides/{id}">client.style_guides.<a href="./src/avido/resources/style_guides.py">retrieve</a>(id) -> <a href="./src/avido/types/style_guide_response.py">StyleGuideResponse</a></code>
- <code title="get /v0/style-guides">client.style_guides.<a href="./src/avido/resources/style_guides.py">list</a>(\*\*<a href="src/avido/types/style_guide_list_params.py">params</a>) -> <a href="./src/avido/types/style_guide.py">SyncOffsetPagination[StyleGuide]</a></code>

# Documents

Types:

```python
from avido.types import (
    Document,
    DocumentChunk,
    DocumentResponse,
    DocumentStatus,
    DocumentListResponse,
)
```

Methods:

- <code title="post /v0/documents">client.documents.<a href="./src/avido/resources/documents.py">create</a>(\*\*<a href="src/avido/types/document_create_params.py">params</a>) -> <a href="./src/avido/types/document_response.py">DocumentResponse</a></code>
- <code title="get /v0/documents/{id}">client.documents.<a href="./src/avido/resources/documents.py">retrieve</a>(id) -> <a href="./src/avido/types/document_response.py">DocumentResponse</a></code>
- <code title="get /v0/documents">client.documents.<a href="./src/avido/resources/documents.py">list</a>(\*\*<a href="src/avido/types/document_list_params.py">params</a>) -> <a href="./src/avido/types/document_list_response.py">SyncOffsetPagination[DocumentListResponse]</a></code>
- <code title="get /v0/documents/chunked">client.documents.<a href="./src/avido/resources/documents.py">list_chunks</a>(\*\*<a href="src/avido/types/document_list_chunks_params.py">params</a>) -> <a href="./src/avido/types/document_chunk.py">SyncOffsetPagination[DocumentChunk]</a></code>
