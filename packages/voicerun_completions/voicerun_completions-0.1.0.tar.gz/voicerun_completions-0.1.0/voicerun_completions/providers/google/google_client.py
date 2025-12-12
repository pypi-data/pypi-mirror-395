from typing import Any, AsyncIterator, Optional
from google.genai import Client
from google.genai.types import (
    Candidate as GoogleResponseCandidate,
    Content as GoogleMessageContent,
    Part as GoogleMessagePart,
    GenerateContentResponse as GoogleContentResponse,
    GenerateContentConfigDict as GoogleRequestConfigDict,
    ThinkingConfigDict as GoogleThinkingConfigDict,
)
from primfunctions.completions.messages import AssistantMessage, FunctionCall, ToolCall
from primfunctions.completions.response import ChatCompletionResponse
from primfunctions.completions.request import ChatCompletionRequest, StreamOptions

from ..base import CompletionClient
from .utils import denormalize_conversation_history, denormalize_tools, denormalize_tool_choice
from .streaming import GoogleStreamProcessor


class GoogleCompletionClient(CompletionClient):

    def _denormalize_request(
        self,
        request: ChatCompletionRequest,
    ) -> dict[str, Any]:
        """Convert ChatCompletionRequest to kwargs for _get_completion."""

        contents, system_instruction = denormalize_conversation_history(request.messages)

        kwargs = {
            "api_key": request.api_key,
            "model": request.model,
            "contents": contents,
        }

        # Build config using GenerateContentConfigDict
        config_dict = {}

        if request.temperature is not None:
            config_dict["temperature"] = request.temperature

        if request.max_tokens is not None:
            config_dict["max_output_tokens"] = request.max_tokens

        if request.tools:
            config_dict["tools"] = denormalize_tools(request.tools)

        if request.tool_choice:
            tool_config = denormalize_tool_choice(request.tool_choice)
            if tool_config:
                config_dict["tool_config"] = tool_config
        
        if request.timeout is not None:
            # Google takes timeout in ms
            timeout_ms: int = request.timeout * 1000
            config_dict["http_options"] = {
                "timeout": timeout_ms
            }

        # Add system instruction if present
        if system_instruction:
            config_dict["system_instruction"] = system_instruction

        # Disable thinking to improve streaming latency
        config_dict["thinking_config"] = GoogleThinkingConfigDict(
            thinking_budget=0,  # 0 = DISABLED
            include_thoughts=False
        )

        # Only add config if it has values
        if config_dict:
            kwargs["config"] = GoogleRequestConfigDict(**config_dict)

        return kwargs

    def _normalize_response(
        self,
        response: GoogleContentResponse,
    ) -> ChatCompletionResponse:

        # Take only first candidate
        candidate: GoogleResponseCandidate = response.candidates[0]
        google_message: GoogleMessageContent = candidate.content
        google_message_parts: list[GoogleMessagePart] = google_message.parts

        # Extract text and function calls from parts
        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []
        tool_call_index: int = 0

        for part in google_message_parts:
            if part.text:
                text_parts.append(part.text)
            elif part.function_call:
                # Convert function call to ToolCall
                tool_calls.append(ToolCall(
                    id=part.function_call.id,
                    type="function",
                    function=FunctionCall(
                        name=part.function_call.name,
                        arguments=part.function_call.args
                    ),
                    index=tool_call_index,
                ))
                tool_call_index += 1

        # Combine text content
        content = "".join(text_parts) if text_parts else None

        normalized_message = AssistantMessage(
            content=content,
            tool_calls=tool_calls if tool_calls else None
        )

        return ChatCompletionResponse(
            message=normalized_message,
            finish_reason=candidate.finish_reason,
            usage=response.usage_metadata.model_dump() if response.usage_metadata else None
        )

    async def _get_completion(
        self,
        api_key: str,
        model: str,
        contents: list[GoogleMessageContent],
        config: Optional[GoogleRequestConfigDict] = None,
    ) -> GoogleContentResponse:
        """Generate content using Google Gen AI client.

        [Client](https://github.com/googleapis/python-genai)
        """

        async with Client(api_key=api_key).aio as async_client:
            return await async_client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )


    def _get_stream_processor(
        self,
        stream_options: Optional[StreamOptions] = None,
    ) -> GoogleStreamProcessor:
        """Get anthropic-specific StreamProcessor."""
        return GoogleStreamProcessor(stream_options=stream_options)


    async def _get_completion_stream(
        self,
        api_key: str,
        model: str,
        contents: list[GoogleMessageContent],
        config: Optional[GoogleRequestConfigDict] = None,
    ) -> AsyncIterator[GoogleContentResponse]:
        """Stream chat completion events from Google.

        [Client](https://github.com/googleapis/python-genai)
        """
        client = Client(api_key=api_key)
        return await client.aio.models.generate_content_stream(
            model=model,
            contents=contents,
            config=config,
        )
