import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, AsyncIterable, Optional
from primfunctions.completions.streaming import ChatCompletionChunk
from primfunctions.completions.response import ChatCompletionResponse
from primfunctions.completions.request import ChatCompletionRequest, StreamOptions
from primfunctions.completions.messages import ToolCall, FunctionCall


@dataclass
class PartialToolCall:
    """Internal state for accumulating tool call data."""
    id: str
    type: str
    function_name: str
    arguments_buffer: str = ""
    index: Optional[int] = None

    def is_complete(self) -> bool:
        """Check if the accumulated arguments form valid JSON."""
        # TODO: better way of doing this?
        try:
            json.loads(self.arguments_buffer)
            return True
        except json.JSONDecodeError:
            return False
        
    def to_tool_call(self) -> ToolCall:
        """Convert this partial to ToolCall. Invalid if not complete."""
        return ToolCall(
            id=self.id,
            type=self.type,
            function=FunctionCall(
                name=self.function_name,
                arguments=json.loads(self.arguments_buffer),
            ),
            index=self.index,
        )


class StreamProcessor(ABC):
    """Processes LLM provider specific completion stream and returns ChatCompletionChunks to yield to client.
    Accumulates streaming tool call deltas and emits complete tool calls.
    """

    @abstractmethod
    async def process_stream(
        self,
        stream: AsyncIterable[Any]
    ) -> AsyncIterable[ChatCompletionChunk]:
        """Process a stream of provider completion chunks and yield normalized chunks."""
        pass


class CompletionClient(ABC):
    """Abstract base class for LLM completion clients."""

    @abstractmethod
    def _denormalize_request(
        self,
        request: ChatCompletionRequest,
    ) -> dict[str, Any]:
        pass


    @abstractmethod
    def _normalize_response(
        self,
        response: Any,
    ) -> ChatCompletionResponse:
        pass


    @abstractmethod
    async def _get_completion(
        self,
        **kwargs
    ) -> Any:
        pass


    @abstractmethod
    async def _get_completion_stream(
        self,
        **kwargs
    ) -> AsyncIterable[Any]:
        """Get streaming completion from provider."""
        pass


    @abstractmethod
    def _get_stream_processor(
        self,
        stream_options: Optional[StreamOptions] = None,
    ) -> StreamProcessor:
        """Get provider-specific StreamProcessor."""
        pass


    async def generate_chat_completion(
        self,
        request: ChatCompletionRequest,
    ) -> ChatCompletionResponse:
        """
        Generate chat completion.

        Args:
            request: Normalized chat completion request

        Returns:
            ChatCompletionResponse with normalized data
        """
        denormalized_request = self._denormalize_request(request)
        completion = await self._get_completion(**denormalized_request)
        return self._normalize_response(completion)


    async def generate_chat_completion_stream(
        self,
        request: ChatCompletionRequest,
    ) -> AsyncIterable[ChatCompletionChunk]:
        """
        Generate streaming chat completion.

        Args:
            request: Normalized chat completion request with streaming=True

        Returns:
            AsyncIterable of ChatCompletionStreamChunk with normalized data
        """
        denormalized_request = self._denormalize_request(request)
        processor = self._get_stream_processor(request.stream_options)
        completion_stream = await self._get_completion_stream(**denormalized_request)

        async for normalized_chunk in processor.process_stream(completion_stream):
            yield normalized_chunk
