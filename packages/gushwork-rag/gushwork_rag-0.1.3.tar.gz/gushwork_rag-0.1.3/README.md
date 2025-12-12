# Gushwork RAG Python SDK

A fully typed Python client for the Gushwork Retrieval-Augmented Generation (RAG) API. The SDK mirrors Pinecone’s ergonomics while exposing every Gushwork resource—namespaces, files, chat, assistants, and API keys—through Pythonic, well-documented clients.

## Features

- 🔐 **API key management** – Create, list, and revoke keys with role-based access.
- 📁 **File pipeline** – Presigned uploads, status updates, and listing helpers (plus S3 bulk ingestion).
- 🗂️ **Namespace management** – CRUD helpers that map to server namespaces/assistants.
- 🤖 **High-level Assistant API** – Pinecone-style façade with retries, S3 folder sync, and cached metadata.
- 💬 **Chat completions** – Sync or streaming responses with retrieval controls (`top_k`, `top_n`, `top_p`) and typed message models.
- 📊 **Structured output & enums** – Strongly typed models for requests/responses, file states, and access levels.
- 🧰 **Utilities & context manager** – HTTP session lifecycle helpers, S3 download utility, and comprehensive error classes.

## Requirements

- Python 3.8+
- Runtime deps (declared in `pyproject.toml`): `requests>=2.25.0`, `boto3>=1.26.0`, `backoff>=2.2.0`
- Optional dev extras (`pip install "gushwork-rag[dev]"`): pytest, coverage, black, isort, mypy, flake8

## Installation

### Stable release

```bash
pip install gushwork-rag
```

### Development / local editing

The SDK uses `pyproject.toml` as the single source of truth for dependencies. Install editable bits plus dev tooling with:

```bash
pip install -e ".[dev]"
```

## Quick Start

### Basic operations

```python
from gushwork_rag import GushworkRAG

# Initialize the client
client = GushworkRAG(
    api_key="your-api-key-here",
    base_url="http://localhost:8080"  # or your production URL
)

# Create a namespace
namespace = client.namespaces.create(
    name="my-documents",
    instructions="Answer questions based on the provided documents."
)

# Upload a file
file = client.files.upload(
    file_path="document.pdf",
    namespace="my-documents"
)

# Chat with your documents
response = client.chat.create(
    namespace="my-documents",
    messages=[
        {"role": "user", "content": "What is the main topic of the document?"}
    ],
    model="gpt-3.5-turbo"
)

print(response.content)
```

### Assistant API (recommended)

The assistant façade mirrors Pinecone’s API while using namespaces under the hood. It automatically retries failed generations (via `backoff` if available) and ships an opinionated S3 ingestion helper.

```python
from gushwork_rag import GushworkRAG

client = GushworkRAG(
    api_key="your-api-key-here",
    base_url="http://localhost:8080"
)

# Create an assistant
assistant = client.assistant.create_assistant(
    assistant_name="my-assistant",
    instructions="Answer questions based on the provided documents."
)

# Get an assistant
assistant = client.assistant("my-assistant")

# Generate a response
response = assistant.generate_response(
    prompt="What is this document about?",
    model="gpt-3.5-turbo"
)
print(response)

# List files in the assistant
files = assistant.list_files()
print(f"Files: {len(files.files)}")

# Upload files from S3 folder
assistant.upload_s3_folder(
    bucket_name="my-bucket",
    folder_path="documents/folder",
    exclude=None,  # Optional: list of filenames to exclude
    max_workers=10,  # Number of parallel uploads
    rate_limit_delay=5.0,  # Delay between uploads
)

# Delete the assistant
assistant.delete_assistant()
```

## Usage Examples

### Context manager (recommended)

```python
from gushwork_rag import GushworkRAG

with GushworkRAG(api_key="your-api-key") as client:
    # Your code here
    health = client.health_check()
    print(health["status"])
# Client is automatically closed
```

### Managing namespaces

```python
# Create a namespace
namespace = client.namespaces.create(
    name="research-papers",
    instructions="Provide scientific and accurate answers based on research papers."
)

# List all namespaces
namespaces = client.namespaces.list()
for ns in namespaces:
    print(f"{ns.name}: {ns.instructions}")

# Get a specific namespace
namespace = client.namespaces.get(namespace_id="ns_123")

# Update a namespace
updated = client.namespaces.update(
    namespace_id="ns_123",
    instructions="New instructions here"
)

# Delete a namespace
client.namespaces.delete(namespace_id="ns_123")
```

### File operations

```python
# Upload a file
file = client.files.upload(
    file_path="path/to/document.pdf",
    namespace="my-documents",
    mime_type="application/pdf"  # Optional, auto-detected
)
print(f"Uploaded: {file.file_name}")

# List files in a namespace
files = client.files.list_by_namespace(
    namespace="my-documents",
    limit=50,
    skip=0
)
print(f"Total files: {files.total}")
for file in files.files:
    print(f"- {file.file_name} ({file.status})")

# Get file details
file = client.files.get(file_id="file_123")
print(f"Status: {file.status}")
print(f"Uploaded: {file.uploaded_at}")

# Update file status (typically for internal use)
from gushwork_rag import FileStatus

file = client.files.update_status(
    file_id="file_123",
    status=FileStatus.FILE_INDEXED,
    processed_at="2024-01-01T00:00:00Z"
)

# Delete a file
client.files.delete(file_id="file_123")
```

### Chat completions

#### Simple chat

```python
response = client.chat.create(
    namespace="my-documents",
    messages=[
        {"role": "user", "content": "What are the key findings?"}
    ],
    model="gpt-3.5-turbo"
)
print(response.content)
```

#### Multi-turn conversation

```python
from gushwork_rag import Message

messages = [
    Message(role="user", content="What is the document about?"),
    Message(role="assistant", content="The document discusses AI technologies."),
    Message(role="user", content="What are the main benefits mentioned?"),
]

response = client.chat.create(
    namespace="my-documents",
    messages=messages,
    model="gpt-4"
)
print(response.content)
```

#### Streaming chat

```python
# Stream responses in real-time
for chunk in client.chat.stream(
    namespace="my-documents",
    messages=[{"role": "user", "content": "Summarize the document"}],
    model="gpt-3.5-turbo"
):
    content = chunk.get("content", "")
    print(content, end="", flush=True)
print()  # New line at the end
```

#### Structured output

```python
# Get responses in a specific JSON format
response = client.chat.create(
    namespace="my-documents",
    messages=[{"role": "user", "content": "Extract key information"}],
    model="gpt-4",
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "document_summary",
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "summary": {"type": "string"},
                    "key_points": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["title", "summary", "key_points"]
            }
        }
    }
)
print(response.content)  # Returns a dictionary matching the schema
```

#### Advanced retrieval options

```python
from gushwork_rag import RetrievalType

response = client.chat.create(
    namespace="my-documents",
    messages=[{"role": "user", "content": "What are the conclusions?"}],
    model="gpt-3.5-turbo",
    retrieval_type=RetrievalType.GEMINI,  # or RetrievalType.SIMPLE
    top_k=10,  # Number of top results to retrieve
    top_n=5,   # Number of top chunks to return
    top_p=0.9  # Top-p sampling parameter
)
```

### Assistant workflows

The assistant wrapper adds retries, cached namespace metadata, and an opinionated `upload_s3_folder()` helper that deduplicates against existing files before downloading from S3.

```python
# Create an assistant using AssistantCreator
assistant = client.assistant

# Create a new assistant
assistant = assistant.create_assistant(
    assistant_name="my-assistant",
    instructions="Answer questions based on the provided documents."
)

# Get an assistant
assistant = client.assistant("my-assistant")

# Generate a response (with automatic retries)
response = assistant.generate_response(
    prompt="What is this document about?",
    model="gpt-3.5-turbo",
    max_retries=3  # Optional: number of retries on failure
)
print(response)

# List files in the assistant
files = assistant.list_files(limit=50, skip=0)
print(f"Total files: {files.total}")
for file in files.files:
    print(f"- {file.file_name}")

# Upload files from S3 folder (with deduplication)
assistant.upload_s3_folder(
    bucket_name="my-bucket",
    folder_path="documents/folder",
    exclude=["file1.pdf", "file2.pdf"],  # Optional: files to exclude
    max_workers=10,  # Parallel upload workers
    rate_limit_delay=5.0,  # Delay between uploads (seconds)
)

# Delete the assistant
assistant.delete_assistant()
```

### API key management (requires ADMIN access)

```python
from gushwork_rag import APIAccess

# Create a new API key
api_key = client.auth.create_api_key(
    key_name="production-key",
    access=APIAccess.READ_WRITE
)
print(f"New API Key: {api_key.api_key}")
# Save this key securely!

# List all API keys
keys = client.auth.list_api_keys()
for key in keys:
    print(f"{key.key_name}: {key.access} (Last used: {key.last_used})")

# Delete an API key
client.auth.delete_api_key(api_key_id="key_123")
```

## API Reference

### `GushworkRAG`

Main client class for interacting with the API.

**Properties:**
- `namespaces` - NamespacesClient for managing namespaces
- `files` - FilesClient for managing files
- `chat` - ChatClient for chat completions
- `auth` - AuthClient for API key management
- `assistant_` - Assistant for creating assistants

**Methods:**
- `health_check()` - Check API health
- `assistant(assistant_name)` - Get an Assistant client for a specific assistant
- `close()` - Close the HTTP session

### `AssistantCreator`

Create and manage assistants (namespaces).

**Methods:**
- `create_assistant(assistant_name, instructions)` - Create a new assistant

### `Assistant`

Manage a specific assistant (namespace).

**Methods:**
- `generate_response(prompt, model, max_retries)` - Generate a response with automatic retries
- `list_files(limit, skip)` - List files in the assistant
- `upload_s3_folder(bucket_name, folder_path, exclude, max_workers, rate_limit_delay)` - Upload files from S3
- `delete_assistant()` - Delete the assistant
- `name` - Property: Get the assistant name
- `namespace` - Property: Get the namespace object

### `NamespacesClient`

Manage document namespaces.

**Methods:**
- `create(name, instructions)` - Create a namespace
- `list()` - List all namespaces
- `get(namespace_id)` - Get a namespace by ID
- `update(namespace_id, instructions)` - Update a namespace
- `delete(namespace_id)` - Delete a namespace

### `FilesClient`

Manage files and documents.

**Methods:**
- `upload(file_path, namespace, mime_type)` - Upload a file
- `get(file_id)` - Get file details
- `list_by_namespace(namespace, limit, skip)` - List files in a namespace
- `update_status(file_id, status, ...)` - Update file status
- `delete(file_id)` - Delete a file

### `ChatClient`

Chat completions with RAG.

**Methods:**
- `create(namespace, messages, model, **kwargs)` - Get a chat completion
- `stream(namespace, messages, model, **kwargs)` - Stream a chat completion
- `completions(namespace, messages, model, **kwargs)` - Generic completion method

### `AuthClient`

Manage API keys (requires ADMIN access).

**Methods:**
- `create_api_key(key_name, access)` - Create a new API key
- `list_api_keys()` - List all API keys
- `delete_api_key(api_key_id)` - Delete an API key

