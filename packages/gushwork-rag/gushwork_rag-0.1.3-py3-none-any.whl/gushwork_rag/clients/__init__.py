"""Sub-clients for different API resources."""

from .auth import AuthClient
from .assistant import Assistant, AssistantInstance
from .chat import ChatClient
from .files import FilesClient
from .namespaces import NamespacesClient

__all__ = [
    "AuthClient",
    "Assistant",
    "AssistantInstance",
    "ChatClient",
    "FilesClient",
    "NamespacesClient",
]

