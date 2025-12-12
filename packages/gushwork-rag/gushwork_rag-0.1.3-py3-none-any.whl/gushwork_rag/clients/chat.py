"""Client for chat completion operations."""

from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Optional, Union

from ..models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    Message,
    RetrievalType,
)
from ..http_client import HTTPClient


class ChatClient:
    """Client for chat completions with RAG."""
    Message = Message

    
    def __init__(self, http_client: "HTTPClient"):
        self._http = http_client

    def completions(
        self,
        namespace: str,
        messages: List[Union[Message, Dict[str, str]]],
        model: str = "gpt-3.5-turbo",
        retrieval_type: RetrievalType = RetrievalType.GEMINI,
        top_k: Optional[int] = None,
        top_n: Optional[int] = None,
        top_p: Optional[float] = None,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> Union[ChatCompletionResponse, Iterator[Dict[str, Any]]]:
        # Convert dict messages to Message objects
        parsed_messages = []
        for msg in messages:
            if isinstance(msg, dict):
                parsed_messages.append(Message(role=msg["role"], content=msg["content"]))
            else:
                parsed_messages.append(msg)

        request = ChatCompletionRequest(
            namespace=namespace,
            messages=parsed_messages,
            model=model,
            retrieval_type=retrieval_type,
            top_k=top_k,
            top_n=top_n,
            top_p=top_p,
            response_format=response_format,
        )


        response = self._http.post("/api/v1/chat/completions", request.to_dict())
        return ChatCompletionResponse.from_dict(response)

    def create(
        self,
        namespace: str,
        messages: List[Union[Message, Dict[str, str]]],
        model: str = "gpt-3.5-turbo",
        **kwargs: Any,
    ) -> ChatCompletionResponse:
        """
        Create a chat completion (alias for completions without streaming).

        Args:
            namespace: Namespace containing the documents
            messages: List of messages
            model: Model to use
            **kwargs: Additional arguments passed to completions()

        Returns:
            ChatCompletionResponse

        Raises:
            NotFoundError: If namespace not found
            AuthenticationError: If authentication fails
            BadRequestError: If request parameters are invalid
        """
        result = self.completions(namespace, messages, model, **kwargs)
        if not isinstance(result, ChatCompletionResponse):
            raise TypeError("Expected ChatCompletionResponse but got streaming iterator")
        return result

    