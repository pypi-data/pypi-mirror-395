# SDK Architecture



## Design Philosophy

The SDK follows these principles:

1. **Pythonic API**: Clean, intuitive interfaces following Python best practices
2. **Type Safety**: Full type hints for IDE integration and type checking
3. **Resource-Based**: Organized around resources (files, namespaces, etc.)
4. **Modular**: Separation of concerns with sub-clients
5. **Error Handling**: Clear, descriptive exceptions
6. **Extensible**: Easy to add new features

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│              GushworkRAG (Main Client)          │
│  ┌───────────────────────────────────────────┐  │
│  │         HTTPClient (HTTP Layer)           │  │
│  └───────────────────────────────────────────┘  │
│                      │                          │
│       ┌──────────────┼──────────────┐          │
│       │              │              │          │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐     │
│  │ Files   │   │  Chat   │   │  Auth   │ ... │
│  │ Client  │   │ Client  │   │ Client  │     │
│  └─────────┘   └─────────┘   └─────────┘     │
└─────────────────────────────────────────────────┘
         │              │              │
         └──────────────┼──────────────┘
                        │
                   API Server
```

## Core Components

### 1. Main Client (`GushworkRAG`)

The entry point for all SDK operations. Similar to Pinecone's main client.

**Responsibilities:**
- Initialize HTTP client
- Provide access to sub-clients
- Manage session lifecycle

**Design Pattern:** Facade Pattern

```python
class GushworkRAG:
    def __init__(self, api_key, base_url):
        self._http = HTTPClient(api_key, base_url)
        self._files = FilesClient(self._http)
        self._chat = ChatClient(self._http)
        # ... more clients
    
    @property
    def files(self) -> FilesClient:
        return self._files
```

**Comparison with Pinecone:**
```python
# Pinecone
client = Pinecone(api_key="...")
index = client.Index("index-name")

# Gushwork RAG
client = GushworkRAG(api_key="...")
files = client.files
```

### 2. HTTP Client (`HTTPClient`)

Handles all HTTP communication with the API.

**Responsibilities:**
- Make HTTP requests
- Handle authentication
- Error handling and retry logic
- Streaming support

**Design Pattern:** Adapter Pattern

```python
class HTTPClient:
    def request(self, method, endpoint, data=None):
        # Handle request, errors, etc.
        pass
    
    def request_stream(self, method, endpoint, data=None):
        # Handle streaming responses
        pass
```

### 3. Sub-Clients

Resource-specific clients for different API operations.

#### FilesClient

Manages file operations:
- Upload files (with S3 presigned URLs)
- List files
- Get file details
- Update status
- Delete files

#### ChatClient

Handles chat completions:
- Create completions
- Stream responses
- Handle structured output
- Support retrieval options

#### NamespacesClient

Manages namespaces:
- Create namespaces
- List/get namespaces
- Update namespaces
- Delete namespaces

#### AuthClient

API key management:
- Create API keys
- List API keys
- Delete API keys

### 4. Models (`models.py`)

Data classes representing API resources.

**Design Pattern:** Data Transfer Objects (DTOs)

```python
@dataclass
class File:
    file_name: str
    namespace: str
    status: FileStatus
    # ... other fields
    
    @classmethod
    def from_dict(cls, data: Dict) -> "File":
        # Parse API response
        pass
```

**Key Features:**
- Type hints for all fields
- `from_dict()` class methods for parsing
- Enums for status values
- DateTime handling

### 5. Exceptions (`exceptions.py`)

Custom exception hierarchy for error handling.

**Design Pattern:** Exception Hierarchy

```
GushworkError (Base)
├── AuthenticationError (401)
├── ForbiddenError (403)
├── NotFoundError (404)
├── BadRequestError (400)
└── ServerError (500)
```

## Request Flow

1. **User calls method on client**
   ```python
   file = client.files.upload("doc.pdf", "namespace")
   ```

2. **Sub-client prepares request**
   ```python
   # FilesClient
   data = {"fileName": "doc.pdf", "namespace": "namespace"}
   response = self._http.post("/api/v1/files/upload", data)
   ```

3. **HTTPClient makes request**
   ```python
   # HTTPClient
   response = self.session.request("POST", url, json=data)
   if not response.ok:
       self._handle_error(response)
   ```

4. **Response parsed into model**
   ```python
   # FilesClient
   return File.from_dict(response)
   ```

5. **User receives typed object**
   ```python
   # User code
   print(file.file_name)  # IDE autocomplete works!
   ```


## Design Decisions

### 1. Properties vs Methods for Sub-clients

**Chosen:** Properties (`client.files`)

**Reasoning:**
- More intuitive (`client.files.upload()`)
- Consistent access pattern
- Lazy initialization possible
- Similar to Pinecone's approach

```python
# Property approach (chosen)
client.files.upload("doc.pdf")

# Method approach (alternative)
client.get_files_client().upload("doc.pdf")
```

### 2. Dataclasses vs Pydantic

**Chosen:** Dataclasses

**Reasoning:**
- Built-in to Python 3.7+
- No external dependencies
- Good enough for our use case
- Lightweight

**Trade-offs:**
- Less validation than Pydantic
- Manual `from_dict()` methods
- No automatic JSON serialization

### 3. Synchronous vs Async

**Chosen:** Synchronous (for now)

**Reasoning:**
- Simpler to use
- Covers most use cases
- Can add async later

**Future:** Consider async version:
```python
# Future async API
async with GushworkRAGAsync(api_key="...") as client:
    file = await client.files.upload("doc.pdf")
```

### 4. Error Handling Strategy

**Chosen:** Custom exception hierarchy

**Reasoning:**
- Specific exceptions for specific errors
- Easy to catch and handle
- Clear error messages
- Status codes preserved

```python
try:
    file = client.files.get("id")
except NotFoundError:
    # Handle 404
    pass
except AuthenticationError:
    # Handle 401
    pass
```

### 5. Streaming Implementation

**Chosen:** Iterator pattern

**Reasoning:**
- Pythonic (for loops work naturally)
- Memory efficient
- Easy to use

```python
for chunk in client.chat.stream(...):
    print(chunk.get("content"))
```

## Extensibility

### Adding New Endpoints

1. **Create model** (if needed)
   ```python
   @dataclass
   class NewResource:
       field: str
       
       @classmethod
       def from_dict(cls, data):
           return cls(field=data["field"])
   ```

2. **Create client**
   ```python
   class NewResourceClient:
       def __init__(self, http_client):
           self._http = http_client
       
       def create(self, field: str) -> NewResource:
           response = self._http.post("/api/v1/resource", {"field": field})
           return NewResource.from_dict(response)
   ```

3. **Add to main client**
   ```python
   class GushworkRAG:
       def __init__(self, ...):
           # ...
           self._new_resource = NewResourceClient(self._http)
       
       @property
       def new_resource(self) -> NewResourceClient:
           return self._new_resource
   ```

### Adding New Features

- **Batch operations**: Add methods to clients
- **Async support**: Create parallel `async` version
- **Caching**: Add caching layer to HTTPClient
- **Retry logic**: Enhance HTTPClient with retries
- **Webhooks**: Add webhook client
- **Metrics**: Add telemetry/metrics

## Testing Strategy

### Unit Tests
- Mock HTTPClient
- Test each client independently
- Test model parsing
- Test error handling

### Integration Tests
- Test against real API (dev environment)
- Test complete workflows
- Test error scenarios

### Example Structure
```python
def test_files_upload(mock_http_client):
    client = FilesClient(mock_http_client)
    mock_http_client.post.return_value = {"url": "s3://..."}
    
    result = client.upload("test.pdf", "namespace")
    
    assert mock_http_client.post.called
    assert result.file_name == "test.pdf"
```

## Performance Considerations

1. **Connection Pooling**: `requests.Session` for connection reuse
2. **Streaming**: Iterator pattern for memory efficiency
3. **Lazy Loading**: Properties create clients on first access
4. **Type Checking**: Runtime overhead minimal with type hints

## Security

1. **API Key Storage**: Never log or print API keys
2. **HTTPS**: Use HTTPS in production
3. **Validation**: Validate inputs before sending
4. **Secrets**: Use environment variables

## Future Enhancements

1. **Async Version**: Full async/await support
2. **Retry Logic**: Automatic retries with exponential backoff
3. **Rate Limiting**: Built-in rate limit handling
4. **Caching**: Response caching for repeated requests
5. **Batch Operations**: Bulk upload/delete
6. **Webhooks**: Event-driven notifications
7. **Metrics**: Usage statistics and telemetry
8. **Plugin System**: Extensible with plugins

## Conclusion

The SDK is designed to be:
- **Easy to use**: Intuitive API
- **Type safe**: Full type hints
- **Extensible**: Easy to add features
- **Maintainable**: Clean separation of concerns
- **Pythonic**: Following Python best practices

This architecture provides a solid foundation for the SDK while remaining flexible for future enhancements.

