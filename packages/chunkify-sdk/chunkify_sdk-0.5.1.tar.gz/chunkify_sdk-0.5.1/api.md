# Shared Types

```python
from chunkify.types import ChunkifyError
```

# Files

Types:

```python
from chunkify.types import APIFile
```

Methods:

- <code title="get /api/files/{fileId}">client.files.<a href="./src/chunkify/resources/files.py">retrieve</a>(file_id) -> <a href="./src/chunkify/types/api_file.py">APIFile</a></code>
- <code title="get /api/files">client.files.<a href="./src/chunkify/resources/files.py">list</a>(\*\*<a href="src/chunkify/types/file_list_params.py">params</a>) -> <a href="./src/chunkify/types/api_file.py">SyncPaginatedResults[APIFile]</a></code>
- <code title="delete /api/files/{fileId}">client.files.<a href="./src/chunkify/resources/files.py">delete</a>(file_id) -> None</code>

# Jobs

Types:

```python
from chunkify.types import HlsAv1, HlsH264, HlsH265, Job, Jpg, MP4Av1, MP4H264, MP4H265, WebmVp9
```

Methods:

- <code title="post /api/jobs">client.jobs.<a href="./src/chunkify/resources/jobs/jobs.py">create</a>(\*\*<a href="src/chunkify/types/job_create_params.py">params</a>) -> <a href="./src/chunkify/types/job.py">Job</a></code>
- <code title="get /api/jobs/{jobId}">client.jobs.<a href="./src/chunkify/resources/jobs/jobs.py">retrieve</a>(job_id) -> <a href="./src/chunkify/types/job.py">Job</a></code>
- <code title="get /api/jobs">client.jobs.<a href="./src/chunkify/resources/jobs/jobs.py">list</a>(\*\*<a href="src/chunkify/types/job_list_params.py">params</a>) -> <a href="./src/chunkify/types/job.py">SyncPaginatedResults[Job]</a></code>
- <code title="delete /api/jobs/{jobId}">client.jobs.<a href="./src/chunkify/resources/jobs/jobs.py">delete</a>(job_id) -> None</code>
- <code title="post /api/jobs/{jobId}/cancel">client.jobs.<a href="./src/chunkify/resources/jobs/jobs.py">cancel</a>(job_id) -> None</code>

## Files

Types:

```python
from chunkify.types.jobs import FileListResponse
```

Methods:

- <code title="get /api/jobs/{jobId}/files">client.jobs.files.<a href="./src/chunkify/resources/jobs/files.py">list</a>(job_id) -> <a href="./src/chunkify/types/jobs/file_list_response.py">FileListResponse</a></code>

## Logs

Types:

```python
from chunkify.types.jobs import LogListResponse
```

Methods:

- <code title="get /api/jobs/{jobId}/logs">client.jobs.logs.<a href="./src/chunkify/resources/jobs/logs.py">list</a>(job_id, \*\*<a href="src/chunkify/types/jobs/log_list_params.py">params</a>) -> <a href="./src/chunkify/types/jobs/log_list_response.py">LogListResponse</a></code>

## Transcoders

Types:

```python
from chunkify.types.jobs import TranscoderListResponse
```

Methods:

- <code title="get /api/jobs/{jobId}/transcoders">client.jobs.transcoders.<a href="./src/chunkify/resources/jobs/transcoders.py">list</a>(job_id) -> <a href="./src/chunkify/types/jobs/transcoder_list_response.py">TranscoderListResponse</a></code>

# Notifications

Types:

```python
from chunkify.types import Notification
```

Methods:

- <code title="post /api/notifications">client.notifications.<a href="./src/chunkify/resources/notifications.py">create</a>(\*\*<a href="src/chunkify/types/notification_create_params.py">params</a>) -> <a href="./src/chunkify/types/notification.py">Notification</a></code>
- <code title="get /api/notifications/{notificationId}">client.notifications.<a href="./src/chunkify/resources/notifications.py">retrieve</a>(notification_id) -> <a href="./src/chunkify/types/notification.py">Notification</a></code>
- <code title="get /api/notifications">client.notifications.<a href="./src/chunkify/resources/notifications.py">list</a>(\*\*<a href="src/chunkify/types/notification_list_params.py">params</a>) -> <a href="./src/chunkify/types/notification.py">SyncPaginatedResults[Notification]</a></code>
- <code title="delete /api/notifications/{notificationId}">client.notifications.<a href="./src/chunkify/resources/notifications.py">delete</a>(notification_id) -> None</code>

# Projects

Types:

```python
from chunkify.types import Project, ProjectListResponse
```

Methods:

- <code title="post /api/projects">client.projects.<a href="./src/chunkify/resources/projects.py">create</a>(\*\*<a href="src/chunkify/types/project_create_params.py">params</a>) -> <a href="./src/chunkify/types/project.py">Project</a></code>
- <code title="get /api/projects/{projectId}">client.projects.<a href="./src/chunkify/resources/projects.py">retrieve</a>(project_id) -> <a href="./src/chunkify/types/project.py">Project</a></code>
- <code title="patch /api/projects/{projectId}">client.projects.<a href="./src/chunkify/resources/projects.py">update</a>(project_id, \*\*<a href="src/chunkify/types/project_update_params.py">params</a>) -> None</code>
- <code title="get /api/projects">client.projects.<a href="./src/chunkify/resources/projects.py">list</a>(\*\*<a href="src/chunkify/types/project_list_params.py">params</a>) -> <a href="./src/chunkify/types/project_list_response.py">ProjectListResponse</a></code>
- <code title="delete /api/projects/{projectId}">client.projects.<a href="./src/chunkify/resources/projects.py">delete</a>(project_id) -> None</code>

# Sources

Types:

```python
from chunkify.types import Source
```

Methods:

- <code title="post /api/sources">client.sources.<a href="./src/chunkify/resources/sources.py">create</a>(\*\*<a href="src/chunkify/types/source_create_params.py">params</a>) -> <a href="./src/chunkify/types/source.py">Source</a></code>
- <code title="get /api/sources/{sourceId}">client.sources.<a href="./src/chunkify/resources/sources.py">retrieve</a>(source_id) -> <a href="./src/chunkify/types/source.py">Source</a></code>
- <code title="get /api/sources">client.sources.<a href="./src/chunkify/resources/sources.py">list</a>(\*\*<a href="src/chunkify/types/source_list_params.py">params</a>) -> <a href="./src/chunkify/types/source.py">SyncPaginatedResults[Source]</a></code>
- <code title="delete /api/sources/{sourceId}">client.sources.<a href="./src/chunkify/resources/sources.py">delete</a>(source_id) -> None</code>

# Storages

Types:

```python
from chunkify.types import Storage, StorageListResponse
```

Methods:

- <code title="post /api/storages">client.storages.<a href="./src/chunkify/resources/storages.py">create</a>(\*\*<a href="src/chunkify/types/storage_create_params.py">params</a>) -> <a href="./src/chunkify/types/storage.py">Storage</a></code>
- <code title="get /api/storages/{storageId}">client.storages.<a href="./src/chunkify/resources/storages.py">retrieve</a>(storage_id) -> <a href="./src/chunkify/types/storage.py">Storage</a></code>
- <code title="get /api/storages">client.storages.<a href="./src/chunkify/resources/storages.py">list</a>() -> <a href="./src/chunkify/types/storage_list_response.py">StorageListResponse</a></code>
- <code title="delete /api/storages/{storageId}">client.storages.<a href="./src/chunkify/resources/storages.py">delete</a>(storage_id) -> None</code>

# Tokens

Types:

```python
from chunkify.types import Token, TokenListResponse
```

Methods:

- <code title="post /api/tokens">client.tokens.<a href="./src/chunkify/resources/tokens.py">create</a>(\*\*<a href="src/chunkify/types/token_create_params.py">params</a>) -> <a href="./src/chunkify/types/token.py">Token</a></code>
- <code title="get /api/tokens">client.tokens.<a href="./src/chunkify/resources/tokens.py">list</a>() -> <a href="./src/chunkify/types/token_list_response.py">TokenListResponse</a></code>
- <code title="delete /api/tokens/{tokenId}">client.tokens.<a href="./src/chunkify/resources/tokens.py">revoke</a>(token_id) -> None</code>

# Uploads

Types:

```python
from chunkify.types import Upload
```

Methods:

- <code title="post /api/uploads">client.uploads.<a href="./src/chunkify/resources/uploads.py">create</a>(\*\*<a href="src/chunkify/types/upload_create_params.py">params</a>) -> <a href="./src/chunkify/types/upload.py">Upload</a></code>
- <code title="get /api/uploads/{uploadId}">client.uploads.<a href="./src/chunkify/resources/uploads.py">retrieve</a>(upload_id) -> <a href="./src/chunkify/types/upload.py">Upload</a></code>
- <code title="get /api/uploads">client.uploads.<a href="./src/chunkify/resources/uploads.py">list</a>(\*\*<a href="src/chunkify/types/upload_list_params.py">params</a>) -> <a href="./src/chunkify/types/upload.py">SyncPaginatedResults[Upload]</a></code>
- <code title="delete /api/uploads/{uploadId}">client.uploads.<a href="./src/chunkify/resources/uploads.py">delete</a>(upload_id) -> None</code>

# Webhooks

Types:

```python
from chunkify.types import Webhook, WebhookListResponse, NewEventWebhookEvent, UnwrapWebhookEvent
```

Methods:

- <code title="post /api/webhooks">client.webhooks.<a href="./src/chunkify/resources/webhooks.py">create</a>(\*\*<a href="src/chunkify/types/webhook_create_params.py">params</a>) -> <a href="./src/chunkify/types/webhook.py">Webhook</a></code>
- <code title="get /api/webhooks/{webhookId}">client.webhooks.<a href="./src/chunkify/resources/webhooks.py">retrieve</a>(webhook_id) -> <a href="./src/chunkify/types/webhook.py">Webhook</a></code>
- <code title="patch /api/webhooks/{webhookId}">client.webhooks.<a href="./src/chunkify/resources/webhooks.py">update</a>(webhook_id, \*\*<a href="src/chunkify/types/webhook_update_params.py">params</a>) -> None</code>
- <code title="get /api/webhooks">client.webhooks.<a href="./src/chunkify/resources/webhooks.py">list</a>() -> <a href="./src/chunkify/types/webhook_list_response.py">WebhookListResponse</a></code>
- <code title="delete /api/webhooks/{webhookId}">client.webhooks.<a href="./src/chunkify/resources/webhooks.py">delete</a>(webhook_id) -> None</code>
