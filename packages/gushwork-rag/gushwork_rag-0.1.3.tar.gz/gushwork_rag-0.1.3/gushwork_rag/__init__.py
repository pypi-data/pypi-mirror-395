"""Gushwork RAG SDK - A Python client for the Gushwork RAG API."""

from .client import GushworkRAG
from .clients import Assistant
from .exceptions import (
    GushworkError,
    AuthenticationError,
    NotFoundError,
    BadRequestError,
    ForbiddenError,
    ServerError,
)
from .models import (
    Namespace,
    File,
    FileStatus,
    Message,
    ChatCompletionRequest,
    ChatCompletionResponse,
    APIKey,
)

__version__ = "0.1.3"
__all__ = [
    "GushworkRAG",  
    "Assistant",
    "GushworkError",
    "AuthenticationError",
    "NotFoundError",
    "BadRequestError",
    "ForbiddenError",
    "ServerError",
    "Namespace",
    "File",
    "FileStatus",
    "Message",
    "ChatCompletionRequest",
    "ChatCompletionResponse",
    "APIKey",
]

