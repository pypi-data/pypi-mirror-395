# Actions

## V1

Types:

```python
from casedev.types.actions import V1CreateResponse, V1ExecuteResponse
```

Methods:

- <code title="post /actions/v1">client.actions.v1.<a href="./src/casedev/resources/actions/v1.py">create</a>(\*\*<a href="src/casedev/types/actions/v1_create_params.py">params</a>) -> <a href="./src/casedev/types/actions/v1_create_response.py">V1CreateResponse</a></code>
- <code title="get /actions/v1/{id}">client.actions.v1.<a href="./src/casedev/resources/actions/v1.py">retrieve</a>(id) -> None</code>
- <code title="get /actions/v1">client.actions.v1.<a href="./src/casedev/resources/actions/v1.py">list</a>() -> None</code>
- <code title="delete /actions/v1/{id}">client.actions.v1.<a href="./src/casedev/resources/actions/v1.py">delete</a>(id) -> None</code>
- <code title="post /actions/v1/{id}/execute">client.actions.v1.<a href="./src/casedev/resources/actions/v1.py">execute</a>(id, \*\*<a href="src/casedev/types/actions/v1_execute_params.py">params</a>) -> <a href="./src/casedev/types/actions/v1_execute_response.py">V1ExecuteResponse</a></code>
- <code title="get /actions/v1/executions/{id}">client.actions.v1.<a href="./src/casedev/resources/actions/v1.py">retrieve_execution</a>(id) -> None</code>

# Compute

## V1

Types:

```python
from casedev.types.compute import V1DeployResponse
```

Methods:

- <code title="post /compute/v1/deploy">client.compute.v1.<a href="./src/casedev/resources/compute/v1/v1.py">deploy</a>(\*\*<a href="src/casedev/types/compute/v1_deploy_params.py">params</a>) -> <a href="./src/casedev/types/compute/v1_deploy_response.py">V1DeployResponse</a></code>
- <code title="get /compute/v1/pricing">client.compute.v1.<a href="./src/casedev/resources/compute/v1/v1.py">get_pricing</a>() -> None</code>
- <code title="get /compute/v1/usage">client.compute.v1.<a href="./src/casedev/resources/compute/v1/v1.py">get_usage</a>(\*\*<a href="src/casedev/types/compute/v1_get_usage_params.py">params</a>) -> None</code>

### Environments

Types:

```python
from casedev.types.compute.v1 import EnvironmentCreateResponse, EnvironmentDeleteResponse
```

Methods:

- <code title="post /compute/v1/environments">client.compute.v1.environments.<a href="./src/casedev/resources/compute/v1/environments.py">create</a>(\*\*<a href="src/casedev/types/compute/v1/environment_create_params.py">params</a>) -> <a href="./src/casedev/types/compute/v1/environment_create_response.py">EnvironmentCreateResponse</a></code>
- <code title="get /compute/v1/environments/{name}">client.compute.v1.environments.<a href="./src/casedev/resources/compute/v1/environments.py">retrieve</a>(name) -> None</code>
- <code title="get /compute/v1/environments">client.compute.v1.environments.<a href="./src/casedev/resources/compute/v1/environments.py">list</a>() -> None</code>
- <code title="delete /compute/v1/environments/{name}">client.compute.v1.environments.<a href="./src/casedev/resources/compute/v1/environments.py">delete</a>(name) -> <a href="./src/casedev/types/compute/v1/environment_delete_response.py">EnvironmentDeleteResponse</a></code>
- <code title="post /compute/v1/environments/{name}/default">client.compute.v1.environments.<a href="./src/casedev/resources/compute/v1/environments.py">set_default</a>(name) -> None</code>

### Functions

Methods:

- <code title="get /compute/v1/functions">client.compute.v1.functions.<a href="./src/casedev/resources/compute/v1/functions.py">list</a>(\*\*<a href="src/casedev/types/compute/v1/function_list_params.py">params</a>) -> None</code>
- <code title="get /compute/v1/functions/{id}/logs">client.compute.v1.functions.<a href="./src/casedev/resources/compute/v1/functions.py">get_logs</a>(id, \*\*<a href="src/casedev/types/compute/v1/function_get_logs_params.py">params</a>) -> None</code>

### Invoke

Types:

```python
from casedev.types.compute.v1 import InvokeRunResponse
```

Methods:

- <code title="post /compute/v1/invoke/{functionId}">client.compute.v1.invoke.<a href="./src/casedev/resources/compute/v1/invoke.py">run</a>(function_id, \*\*<a href="src/casedev/types/compute/v1/invoke_run_params.py">params</a>) -> <a href="./src/casedev/types/compute/v1/invoke_run_response.py">InvokeRunResponse</a></code>

### Runs

Methods:

- <code title="get /compute/v1/runs/{id}">client.compute.v1.runs.<a href="./src/casedev/resources/compute/v1/runs.py">retrieve</a>(id) -> None</code>
- <code title="get /compute/v1/runs">client.compute.v1.runs.<a href="./src/casedev/resources/compute/v1/runs.py">list</a>(\*\*<a href="src/casedev/types/compute/v1/run_list_params.py">params</a>) -> None</code>

### Secrets

Types:

```python
from casedev.types.compute.v1 import SecretCreateResponse
```

Methods:

- <code title="post /compute/v1/secrets">client.compute.v1.secrets.<a href="./src/casedev/resources/compute/v1/secrets.py">create</a>(\*\*<a href="src/casedev/types/compute/v1/secret_create_params.py">params</a>) -> <a href="./src/casedev/types/compute/v1/secret_create_response.py">SecretCreateResponse</a></code>
- <code title="get /compute/v1/secrets">client.compute.v1.secrets.<a href="./src/casedev/resources/compute/v1/secrets.py">list</a>(\*\*<a href="src/casedev/types/compute/v1/secret_list_params.py">params</a>) -> None</code>
- <code title="delete /compute/v1/secrets/{group}">client.compute.v1.secrets.<a href="./src/casedev/resources/compute/v1/secrets.py">delete_group</a>(group, \*\*<a href="src/casedev/types/compute/v1/secret_delete_group_params.py">params</a>) -> None</code>
- <code title="get /compute/v1/secrets/{group}">client.compute.v1.secrets.<a href="./src/casedev/resources/compute/v1/secrets.py">retrieve_group</a>(group, \*\*<a href="src/casedev/types/compute/v1/secret_retrieve_group_params.py">params</a>) -> None</code>
- <code title="put /compute/v1/secrets/{group}">client.compute.v1.secrets.<a href="./src/casedev/resources/compute/v1/secrets.py">update_group</a>(group, \*\*<a href="src/casedev/types/compute/v1/secret_update_group_params.py">params</a>) -> None</code>

# Convert

## V1

Types:

```python
from casedev.types.convert import V1ProcessResponse, V1WebhookResponse
```

Methods:

- <code title="get /convert/v1/download/{id}">client.convert.v1.<a href="./src/casedev/resources/convert/v1/v1.py">download</a>(id) -> BinaryAPIResponse</code>
- <code title="post /convert/v1/process">client.convert.v1.<a href="./src/casedev/resources/convert/v1/v1.py">process</a>(\*\*<a href="src/casedev/types/convert/v1_process_params.py">params</a>) -> <a href="./src/casedev/types/convert/v1_process_response.py">V1ProcessResponse</a></code>
- <code title="post /convert/v1/webhook">client.convert.v1.<a href="./src/casedev/resources/convert/v1/v1.py">webhook</a>(\*\*<a href="src/casedev/types/convert/v1_webhook_params.py">params</a>) -> <a href="./src/casedev/types/convert/v1_webhook_response.py">V1WebhookResponse</a></code>

### Jobs

Methods:

- <code title="get /convert/v1/jobs/{id}">client.convert.v1.jobs.<a href="./src/casedev/resources/convert/v1/jobs.py">retrieve</a>(id) -> None</code>
- <code title="delete /convert/v1/jobs/{id}">client.convert.v1.jobs.<a href="./src/casedev/resources/convert/v1/jobs.py">delete</a>(id) -> None</code>

# Format

## V1

Methods:

- <code title="post /format/v1/document">client.format.v1.<a href="./src/casedev/resources/format/v1/v1.py">create_document</a>(\*\*<a href="src/casedev/types/format/v1_create_document_params.py">params</a>) -> BinaryAPIResponse</code>

### Templates

Types:

```python
from casedev.types.format.v1 import TemplateCreateResponse
```

Methods:

- <code title="post /format/v1/templates">client.format.v1.templates.<a href="./src/casedev/resources/format/v1/templates.py">create</a>(\*\*<a href="src/casedev/types/format/v1/template_create_params.py">params</a>) -> <a href="./src/casedev/types/format/v1/template_create_response.py">TemplateCreateResponse</a></code>
- <code title="get /format/v1/templates/{id}">client.format.v1.templates.<a href="./src/casedev/resources/format/v1/templates.py">retrieve</a>(id) -> None</code>
- <code title="get /format/v1/templates">client.format.v1.templates.<a href="./src/casedev/resources/format/v1/templates.py">list</a>(\*\*<a href="src/casedev/types/format/v1/template_list_params.py">params</a>) -> None</code>

# Llm

Methods:

- <code title="get /llm/config">client.llm.<a href="./src/casedev/resources/llm/llm.py">get_config</a>() -> None</code>

## V1

Methods:

- <code title="post /llm/v1/embeddings">client.llm.v1.<a href="./src/casedev/resources/llm/v1/v1.py">create_embedding</a>(\*\*<a href="src/casedev/types/llm/v1_create_embedding_params.py">params</a>) -> None</code>
- <code title="get /llm/v1/models">client.llm.v1.<a href="./src/casedev/resources/llm/v1/v1.py">list_models</a>() -> None</code>

### Chat

Types:

```python
from casedev.types.llm.v1 import ChatCreateCompletionResponse
```

Methods:

- <code title="post /llm/v1/chat/completions">client.llm.v1.chat.<a href="./src/casedev/resources/llm/v1/chat.py">create_completion</a>(\*\*<a href="src/casedev/types/llm/v1/chat_create_completion_params.py">params</a>) -> <a href="./src/casedev/types/llm/v1/chat_create_completion_response.py">ChatCreateCompletionResponse</a></code>

# Ocr

## V1

Types:

```python
from casedev.types.ocr import V1ProcessResponse
```

Methods:

- <code title="get /ocr/v1/{id}">client.ocr.v1.<a href="./src/casedev/resources/ocr/v1.py">retrieve</a>(id) -> None</code>
- <code title="get /ocr/v1/{id}/download/{type}">client.ocr.v1.<a href="./src/casedev/resources/ocr/v1.py">download</a>(type, \*, id) -> None</code>
- <code title="post /ocr/v1/process">client.ocr.v1.<a href="./src/casedev/resources/ocr/v1.py">process</a>(\*\*<a href="src/casedev/types/ocr/v1_process_params.py">params</a>) -> <a href="./src/casedev/types/ocr/v1_process_response.py">V1ProcessResponse</a></code>

# Search

## V1

Types:

```python
from casedev.types.search import (
    V1AnswerResponse,
    V1ContentsResponse,
    V1ResearchResponse,
    V1SearchResponse,
    V1SimilarResponse,
)
```

Methods:

- <code title="post /search/v1/answer">client.search.v1.<a href="./src/casedev/resources/search/v1.py">answer</a>(\*\*<a href="src/casedev/types/search/v1_answer_params.py">params</a>) -> <a href="./src/casedev/types/search/v1_answer_response.py">V1AnswerResponse</a></code>
- <code title="post /search/v1/contents">client.search.v1.<a href="./src/casedev/resources/search/v1.py">contents</a>(\*\*<a href="src/casedev/types/search/v1_contents_params.py">params</a>) -> <a href="./src/casedev/types/search/v1_contents_response.py">V1ContentsResponse</a></code>
- <code title="post /search/v1/research">client.search.v1.<a href="./src/casedev/resources/search/v1.py">research</a>(\*\*<a href="src/casedev/types/search/v1_research_params.py">params</a>) -> <a href="./src/casedev/types/search/v1_research_response.py">V1ResearchResponse</a></code>
- <code title="get /search/v1/research/{id}">client.search.v1.<a href="./src/casedev/resources/search/v1.py">retrieve_research</a>(id, \*\*<a href="src/casedev/types/search/v1_retrieve_research_params.py">params</a>) -> None</code>
- <code title="post /search/v1/search">client.search.v1.<a href="./src/casedev/resources/search/v1.py">search</a>(\*\*<a href="src/casedev/types/search/v1_search_params.py">params</a>) -> <a href="./src/casedev/types/search/v1_search_response.py">V1SearchResponse</a></code>
- <code title="post /search/v1/similar">client.search.v1.<a href="./src/casedev/resources/search/v1.py">similar</a>(\*\*<a href="src/casedev/types/search/v1_similar_params.py">params</a>) -> <a href="./src/casedev/types/search/v1_similar_response.py">V1SimilarResponse</a></code>

# Vault

Types:

```python
from casedev.types import (
    VaultCreateResponse,
    VaultListResponse,
    VaultIngestResponse,
    VaultSearchResponse,
    VaultUploadResponse,
)
```

Methods:

- <code title="post /vault">client.vault.<a href="./src/casedev/resources/vault/vault.py">create</a>(\*\*<a href="src/casedev/types/vault_create_params.py">params</a>) -> <a href="./src/casedev/types/vault_create_response.py">VaultCreateResponse</a></code>
- <code title="get /vault/{id}">client.vault.<a href="./src/casedev/resources/vault/vault.py">retrieve</a>(id) -> None</code>
- <code title="get /vault">client.vault.<a href="./src/casedev/resources/vault/vault.py">list</a>() -> <a href="./src/casedev/types/vault_list_response.py">VaultListResponse</a></code>
- <code title="post /vault/{id}/ingest/{objectId}">client.vault.<a href="./src/casedev/resources/vault/vault.py">ingest</a>(object_id, \*, id) -> <a href="./src/casedev/types/vault_ingest_response.py">VaultIngestResponse</a></code>
- <code title="post /vault/{id}/search">client.vault.<a href="./src/casedev/resources/vault/vault.py">search</a>(id, \*\*<a href="src/casedev/types/vault_search_params.py">params</a>) -> <a href="./src/casedev/types/vault_search_response.py">VaultSearchResponse</a></code>
- <code title="post /vault/{id}/upload">client.vault.<a href="./src/casedev/resources/vault/vault.py">upload</a>(id, \*\*<a href="src/casedev/types/vault_upload_params.py">params</a>) -> <a href="./src/casedev/types/vault_upload_response.py">VaultUploadResponse</a></code>

## Graphrag

Methods:

- <code title="get /vault/{id}/graphrag/stats">client.vault.graphrag.<a href="./src/casedev/resources/vault/graphrag.py">get_stats</a>(id) -> None</code>
- <code title="post /vault/{id}/graphrag/init">client.vault.graphrag.<a href="./src/casedev/resources/vault/graphrag.py">init</a>(id) -> None</code>

## Objects

Types:

```python
from casedev.types.vault import ObjectCreatePresignedURLResponse
```

Methods:

- <code title="get /vault/{id}/objects/{objectId}">client.vault.objects.<a href="./src/casedev/resources/vault/objects.py">retrieve</a>(object_id, \*, id) -> None</code>
- <code title="get /vault/{id}/objects">client.vault.objects.<a href="./src/casedev/resources/vault/objects.py">list</a>(id) -> None</code>
- <code title="post /vault/{id}/objects/{objectId}/presigned-url">client.vault.objects.<a href="./src/casedev/resources/vault/objects.py">create_presigned_url</a>(object_id, \*, id, \*\*<a href="src/casedev/types/vault/object_create_presigned_url_params.py">params</a>) -> <a href="./src/casedev/types/vault/object_create_presigned_url_response.py">ObjectCreatePresignedURLResponse</a></code>
- <code title="get /vault/{id}/objects/{objectId}/download">client.vault.objects.<a href="./src/casedev/resources/vault/objects.py">download</a>(object_id, \*, id) -> None</code>
- <code title="get /vault/{id}/objects/{objectId}/text">client.vault.objects.<a href="./src/casedev/resources/vault/objects.py">get_text</a>(object_id, \*, id) -> None</code>

# Voice

## Streaming

Methods:

- <code title="get /voice/streaming/url">client.voice.streaming.<a href="./src/casedev/resources/voice/streaming.py">get_url</a>() -> None</code>

## Transcription

Types:

```python
from casedev.types.voice import TranscriptionRetrieveResponse
```

Methods:

- <code title="post /voice/transcription">client.voice.transcription.<a href="./src/casedev/resources/voice/transcription.py">create</a>(\*\*<a href="src/casedev/types/voice/transcription_create_params.py">params</a>) -> None</code>
- <code title="get /voice/transcription/{id}">client.voice.transcription.<a href="./src/casedev/resources/voice/transcription.py">retrieve</a>(id) -> <a href="./src/casedev/types/voice/transcription_retrieve_response.py">TranscriptionRetrieveResponse</a></code>

## V1

Methods:

- <code title="get /voice/v1/voices">client.voice.v1.<a href="./src/casedev/resources/voice/v1/v1.py">list_voices</a>(\*\*<a href="src/casedev/types/voice/v1_list_voices_params.py">params</a>) -> None</code>

### Speak

Methods:

- <code title="post /voice/v1/speak">client.voice.v1.speak.<a href="./src/casedev/resources/voice/v1/speak.py">create</a>(\*\*<a href="src/casedev/types/voice/v1/speak_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="post /voice/v1/speak/stream">client.voice.v1.speak.<a href="./src/casedev/resources/voice/v1/speak.py">stream</a>(\*\*<a href="src/casedev/types/voice/v1/speak_stream_params.py">params</a>) -> BinaryAPIResponse</code>

# Webhooks

## V1

Types:

```python
from casedev.types.webhooks import V1CreateResponse
```

Methods:

- <code title="post /webhooks/v1">client.webhooks.v1.<a href="./src/casedev/resources/webhooks/v1.py">create</a>(\*\*<a href="src/casedev/types/webhooks/v1_create_params.py">params</a>) -> <a href="./src/casedev/types/webhooks/v1_create_response.py">V1CreateResponse</a></code>
- <code title="get /webhooks/v1/{id}">client.webhooks.v1.<a href="./src/casedev/resources/webhooks/v1.py">retrieve</a>(id) -> None</code>
- <code title="get /webhooks/v1">client.webhooks.v1.<a href="./src/casedev/resources/webhooks/v1.py">list</a>() -> None</code>
- <code title="delete /webhooks/v1/{id}">client.webhooks.v1.<a href="./src/casedev/resources/webhooks/v1.py">delete</a>(id) -> None</code>

# Templates

## V1

Types:

```python
from casedev.types.templates import V1ExecuteResponse
```

Methods:

- <code title="get /templates/v1/{id}">client.templates.v1.<a href="./src/casedev/resources/templates/v1.py">retrieve</a>(id) -> None</code>
- <code title="get /templates/v1">client.templates.v1.<a href="./src/casedev/resources/templates/v1.py">list</a>(\*\*<a href="src/casedev/types/templates/v1_list_params.py">params</a>) -> None</code>
- <code title="post /templates/v1/{id}/execute">client.templates.v1.<a href="./src/casedev/resources/templates/v1.py">execute</a>(id, \*\*<a href="src/casedev/types/templates/v1_execute_params.py">params</a>) -> <a href="./src/casedev/types/templates/v1_execute_response.py">V1ExecuteResponse</a></code>
- <code title="get /templates/v1/executions/{id}">client.templates.v1.<a href="./src/casedev/resources/templates/v1.py">retrieve_execution</a>(id) -> None</code>
- <code title="post /templates/v1/search">client.templates.v1.<a href="./src/casedev/resources/templates/v1.py">search</a>(\*\*<a href="src/casedev/types/templates/v1_search_params.py">params</a>) -> None</code>

# Workflows

## V1

Types:

```python
from casedev.types.workflows import (
    V1CreateResponse,
    V1RetrieveResponse,
    V1UpdateResponse,
    V1ListResponse,
    V1DeleteResponse,
    V1DeployResponse,
    V1ExecuteResponse,
    V1ListExecutionsResponse,
    V1RetrieveExecutionResponse,
    V1UndeployResponse,
)
```

Methods:

- <code title="post /workflows/v1">client.workflows.v1.<a href="./src/casedev/resources/workflows/v1.py">create</a>(\*\*<a href="src/casedev/types/workflows/v1_create_params.py">params</a>) -> <a href="./src/casedev/types/workflows/v1_create_response.py">V1CreateResponse</a></code>
- <code title="get /workflows/v1/{id}">client.workflows.v1.<a href="./src/casedev/resources/workflows/v1.py">retrieve</a>(id) -> <a href="./src/casedev/types/workflows/v1_retrieve_response.py">V1RetrieveResponse</a></code>
- <code title="patch /workflows/v1/{id}">client.workflows.v1.<a href="./src/casedev/resources/workflows/v1.py">update</a>(id, \*\*<a href="src/casedev/types/workflows/v1_update_params.py">params</a>) -> <a href="./src/casedev/types/workflows/v1_update_response.py">V1UpdateResponse</a></code>
- <code title="get /workflows/v1">client.workflows.v1.<a href="./src/casedev/resources/workflows/v1.py">list</a>(\*\*<a href="src/casedev/types/workflows/v1_list_params.py">params</a>) -> <a href="./src/casedev/types/workflows/v1_list_response.py">V1ListResponse</a></code>
- <code title="delete /workflows/v1/{id}">client.workflows.v1.<a href="./src/casedev/resources/workflows/v1.py">delete</a>(id) -> <a href="./src/casedev/types/workflows/v1_delete_response.py">V1DeleteResponse</a></code>
- <code title="post /workflows/v1/{id}/deploy">client.workflows.v1.<a href="./src/casedev/resources/workflows/v1.py">deploy</a>(id) -> <a href="./src/casedev/types/workflows/v1_deploy_response.py">V1DeployResponse</a></code>
- <code title="post /workflows/v1/{id}/execute">client.workflows.v1.<a href="./src/casedev/resources/workflows/v1.py">execute</a>(id, \*\*<a href="src/casedev/types/workflows/v1_execute_params.py">params</a>) -> <a href="./src/casedev/types/workflows/v1_execute_response.py">V1ExecuteResponse</a></code>
- <code title="get /workflows/v1/{id}/executions">client.workflows.v1.<a href="./src/casedev/resources/workflows/v1.py">list_executions</a>(id, \*\*<a href="src/casedev/types/workflows/v1_list_executions_params.py">params</a>) -> <a href="./src/casedev/types/workflows/v1_list_executions_response.py">V1ListExecutionsResponse</a></code>
- <code title="get /workflows/v1/executions/{id}">client.workflows.v1.<a href="./src/casedev/resources/workflows/v1.py">retrieve_execution</a>(id) -> <a href="./src/casedev/types/workflows/v1_retrieve_execution_response.py">V1RetrieveExecutionResponse</a></code>
- <code title="delete /workflows/v1/{id}/deploy">client.workflows.v1.<a href="./src/casedev/resources/workflows/v1.py">undeploy</a>(id) -> <a href="./src/casedev/types/workflows/v1_undeploy_response.py">V1UndeployResponse</a></code>
