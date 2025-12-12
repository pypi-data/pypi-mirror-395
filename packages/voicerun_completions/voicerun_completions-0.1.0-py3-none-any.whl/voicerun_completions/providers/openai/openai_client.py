from typing import Any, Optional, AsyncIterable
from openai import AsyncOpenAI
from openai.types.chat import (
  ChatCompletion,
  ChatCompletionMessageParam,
  ChatCompletionFunctionToolParam,
  ChatCompletionToolChoiceOptionParam,
)
from openai.types.chat.chat_completion import (
    Choice as OpenAiChoice,
    ChatCompletionMessage as OpenAiChatCompletionMessage,
)
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk as OpenAiCompletionChunk
from primfunctions.completions.messages import AssistantMessage
from primfunctions.completions.response import ChatCompletionResponse
from primfunctions.completions.request import ChatCompletionRequest, StreamOptions

from .streaming import OpenAiStreamProcessor
from ..base import CompletionClient
from .utils import (
  denormalize_conversation_history,
  denormalize_tools,
  denormalize_tool_choice,
  normalize_tool_calls,
)


class OpenAiCompletionClient(CompletionClient):

    def _denormalize_request(
        self,
        request: ChatCompletionRequest,
    ) -> dict[str, Any]:
        """Convert ChatCompletionRequest to kwargs for _get_completion."""

        kwargs = {
            "api_key": request.api_key,
            "model": request.model,
            "messages": denormalize_conversation_history(request.messages),
            "tools": denormalize_tools(request.tools),
            "tool_choice": denormalize_tool_choice(request.tool_choice),
            "temperature": request.temperature if request.temperature else None,
        }

        if request.max_tokens is not None:
            kwargs["max_tokens"] = request.max_tokens

        if request.timeout is not None:
            kwargs["timeout"] = request.timeout

        return kwargs


    def _normalize_response(
        self,
        response: ChatCompletion,
    ) -> ChatCompletionResponse:
        """Convert OpenAI ChatCompletion to normalized ChatCompletionResponse."""
        # Take only first choice
        choice: OpenAiChoice = response.choices[0]
        openai_message: OpenAiChatCompletionMessage = choice.message

        normalized_message = AssistantMessage(
            content=openai_message.content,
            tool_calls=normalize_tool_calls(openai_message.tool_calls)
        )

        return ChatCompletionResponse(
            message=normalized_message,
            finish_reason=choice.finish_reason,
            usage=response.usage.model_dump() if response.usage else None
        )


    async def _get_completion(
        self,
        api_key: str,
        model: str,
        messages: list[ChatCompletionMessageParam],
        tools: Optional[list[ChatCompletionFunctionToolParam]] = None,
        tool_choice: Optional[ChatCompletionToolChoiceOptionParam] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> ChatCompletion:
        """TODO.

        [Client](https://github.com/openai/openai-python)
        """
        async with AsyncOpenAI(api_key=api_key) as client:
            # Build kwargs dict with only non-None values
            kwargs = {
                "model": model,
                "messages": messages,
                "stream": False,  # TODO: streaming support
            }

            # Only add optional parameters if they're provided
            if tools is not None:
                kwargs["tools"] = tools
            if tool_choice is not None:
                kwargs["tool_choice"] = tool_choice
            if temperature is not None:
                kwargs["temperature"] = temperature
            if max_tokens is not None:
                kwargs["max_tokens"] = max_tokens
            if timeout is not None:
                kwargs["timeout"] = timeout

            return await client.chat.completions.create(**kwargs)


    def _get_stream_processor(
        self,
        stream_options: Optional[StreamOptions] = None,
    ) -> OpenAiStreamProcessor:
        """Get openai-specific StreamProcessor."""
        return OpenAiStreamProcessor(stream_options=stream_options)


    async def _get_completion_stream(
        self,
        api_key: str,
        model: str,
        messages: list[ChatCompletionMessageParam],
        tools: Optional[list[ChatCompletionFunctionToolParam]] = None,
        tool_choice: Optional[ChatCompletionToolChoiceOptionParam] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterable[OpenAiCompletionChunk]:
        """Stream chat completion chunks from OpenAI."""
        client = AsyncOpenAI(api_key=api_key)

        # Build kwargs dict with only non-None values
        kwargs = {
            "model": model,
            "messages": messages,
            "stream": True,  # Enable streaming
            "stream_options": {"include_usage": True},  # Include usage information in stream
        }

        # Only add optional parameters if they're provided
        if tools is not None:
            kwargs["tools"] = tools
        if tool_choice is not None:
            kwargs["tool_choice"] = tool_choice
        if temperature is not None:
            kwargs["temperature"] = temperature
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens
        if timeout is not None:
            kwargs["timeout"] = timeout

        return await client.chat.completions.create(**kwargs)
