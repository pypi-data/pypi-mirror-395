from typing import Any, List, Optional
from anthropic import AsyncAnthropic, AsyncStream
from anthropic.types import (
    Message as AnthropicMessage,
    MessageParam as AnthropicMessageParam,
    TextBlockParam as AnthropicTextBlockParam,
    ToolParam as AnthropicToolDefinition,
    ToolChoiceParam as AnthropicToolChoice,
    TextBlock as AnthropicTextBlock,
    ToolUseBlock as AnthropicToolCall,
    RawMessageStreamEvent as AnthropicStreamEvent,
)
from primfunctions.completions.messages import AssistantMessage, ToolCall, FunctionCall
from primfunctions.completions.response import ChatCompletionResponse
from primfunctions.completions.request import ChatCompletionRequest, StreamOptions

from ..base import CompletionClient
from .utils import denormalize_conversation_history, denormalize_tools, denormalize_tool_choice
from .streaming import AnthropicStreamProcessor


class AnthropicCompletionClient(CompletionClient):

    def _denormalize_request(
        self,
        request: ChatCompletionRequest,
    ) -> dict[str, Any]:
        """Convert ChatCompletionRequest to kwargs for _get_completion."""

        messages, system_prompt = denormalize_conversation_history(request.messages)

        kwargs = {
            "api_key": request.api_key,
            "model": request.model,
            "messages": messages,
            "tools": denormalize_tools(request.tools),
            "tool_choice": denormalize_tool_choice(request.tool_choice),
            "temperature": request.temperature if request.temperature else None,
        }

        # Add system prompt if present
        if system_prompt:
            kwargs["system"] = system_prompt

        # Include or default required max_tokens
        kwargs["max_tokens"] = request.max_tokens if request.max_tokens else 4000

        # Include timeout if provided
        if request.timeout is not None:
            kwargs["timeout"] = request.timeout

        return kwargs


    def _normalize_response(
        self,
        response: AnthropicMessage,
    ) -> ChatCompletionResponse:
        """Convert Anthropic Message to normalized ChatCompletionResponse."""

        # Extract text content and tool calls from content blocks
        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []
        tool_call_index: int = 0

        for block in response.content:
            match block:
                case AnthropicTextBlock():
                    text_parts.append(block.text)
                case AnthropicToolCall():
                    tool_calls.append(ToolCall(
                        id=block.id,
                        type="function",
                        function=FunctionCall(
                            name=block.name,
                            arguments=block.input
                        ),
                        index=tool_call_index,
                    ))
                    tool_call_index += 1

        # Combine text content
        content = "".join(text_parts) if text_parts else None

        # Create normalized message
        normalized_message = AssistantMessage(
            content=content,
            tool_calls=tool_calls if tool_calls else None,
        )

        return ChatCompletionResponse(
            message=normalized_message,
            finish_reason=response.stop_reason,
            usage=response.usage.model_dump() if response.usage else None
        )


    async def _get_completion(
        self,
        api_key: str,
        model: str,
        messages: list[AnthropicMessageParam],
        max_tokens: int,
        tools: Optional[list[AnthropicToolDefinition]] = None,
        tool_choice: Optional[AnthropicToolChoice] = None,
        temperature: Optional[float] = None,
        system: Optional[List[AnthropicTextBlockParam]] = None,
        timeout: Optional[float] = None,
    ) -> AnthropicMessage:
        """TODO.

        [Client](https://github.com/anthropics/anthropic-sdk-python)
        """
        async with AsyncAnthropic(api_key=api_key) as client:
            # Build kwargs dict with required values
            kwargs = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "stream": False,  # TODO: streaming support
            }

            # Only add optional parameters if they're provided
            if tools is not None:
                kwargs["tools"] = tools
            if tool_choice is not None:
                kwargs["tool_choice"] = tool_choice
            if temperature is not None:
                kwargs["temperature"] = temperature
            if system is not None:
                kwargs["system"] = system
            if timeout is not None:
                kwargs["timeout"] = timeout

            return await client.messages.create(**kwargs)


    def _get_stream_processor(
        self,
        stream_options: Optional[StreamOptions] = None,
    ) -> AnthropicStreamProcessor:
        """Get anthropic-specific StreamProcessor."""
        return AnthropicStreamProcessor(stream_options=stream_options)


    async def _get_completion_stream(
        self,
        api_key: str,
        model: str,
        messages: list[AnthropicMessageParam],
        max_tokens: int,
        tools: Optional[list[AnthropicToolDefinition]] = None,
        tool_choice: Optional[AnthropicToolChoice] = None,
        temperature: Optional[float] = None,
        system: Optional[List[AnthropicTextBlockParam]] = None,
        timeout: Optional[float] = None,
    ) -> AsyncStream[AnthropicStreamEvent]:
        """Stream chat response events from Anthropic.

        [Client](https://github.com/anthropics/anthropic-sdk-python)
        """
        client = AsyncAnthropic(api_key=api_key)

        # Build kwargs dict with required values
        kwargs = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": True,
        }

        # Only add optional parameters if they're provided
        if tools is not None:
            kwargs["tools"] = tools
        if tool_choice is not None:
            kwargs["tool_choice"] = tool_choice
        if temperature is not None:
            kwargs["temperature"] = temperature
        if system is not None:
            kwargs["system"] = system
        if timeout is not None:
            kwargs["timeout"] = timeout

        return await client.messages.create(**kwargs)