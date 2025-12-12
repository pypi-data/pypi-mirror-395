from typing import Any, Optional, Union, AsyncIterable
from primfunctions.completions.request import (
    CompletionsProvider,
    ChatCompletionRequest,
    StreamOptions,
    ToolChoice,
    ToolDefinition,
    normalize_tools,
)
from primfunctions.completions.messages import ConversationHistory, normalize_messages
from primfunctions.completions.streaming import ChatCompletionChunk
from primfunctions.completions.response import ChatCompletionResponse

from .providers.base import CompletionClient
from .providers.openai.openai_client import OpenAiCompletionClient
from .providers.anthropic.anthropic_client import AnthropicCompletionClient
from .providers.google.google_client import GoogleCompletionClient


async def generate_chat_completion(
    provider: Union[str, CompletionsProvider],
    api_key: str,
    model: str,
    messages: Union[ConversationHistory, list[dict]],
    *,
    tools: Optional[list[Union[ToolDefinition, dict[str, Any]]]] = None,
    tool_choice: Optional[ToolChoice] = None,
    temperature: Optional[float] = None,
    timeout: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> ChatCompletionResponse:
    """
    Generate chat completion.

    Args:
        provider: LLM provider ("openai", "anthropic", or "google")
        api_key: API key for the provider
        model: Model identifier (provider-specific)
        messages: Conversation history or list of message dicts
        tools: Optional list of tool/function definitions
        tool_choice: Tool choice strategy ("none", "auto", "required", or tool name)
        temperature: Sampling temperature (0.0-2.0)
        timeout: Request timeout in seconds
        max_tokens: Maximum tokens to generate

    Returns:
        ChatCompletionResponse with the complete response
    """

    # Normalize string input to enum
    if isinstance(provider, str):
        try:
            provider = CompletionsProvider(provider.lower())
        except ValueError:
            raise ValueError(f"Invalid provider: {provider}.")

    # Normalize messages to proper message objects
    normalized_messages = normalize_messages(messages)

    # Normalize tools to proper tool objects
    normalized_tools = normalize_tools(tools) if tools else None

    client: CompletionClient
    if provider == CompletionsProvider.OPENAI:
        client = OpenAiCompletionClient()
    elif provider == CompletionsProvider.ANTHROPIC:
        client = AnthropicCompletionClient()
    elif provider == CompletionsProvider.GOOGLE:
        client = GoogleCompletionClient()
    else:
        raise ValueError(f"Invalid provider: {provider}")

    request = ChatCompletionRequest(
        provider=provider,
        api_key=api_key,
        model=model,
        messages=normalized_messages,
        tools=normalized_tools,
        tool_choice=tool_choice,
        temperature=temperature,
        timeout=timeout,
        max_tokens=max_tokens,
        streaming=False,
    )

    return await client.generate_chat_completion(request=request)


async def generate_chat_completion_stream(
    provider: Union[str, CompletionsProvider],
    api_key: str,
    model: str,
    messages: Union[ConversationHistory, list[dict]],
    *,
    tools: Optional[list[Union[ToolDefinition, dict[str, Any]]]] = None,
    tool_choice: Optional[ToolChoice] = None,
    temperature: Optional[float] = None,
    timeout: Optional[float] = None,
    max_tokens: Optional[int] = None,
    stream_options: Optional[Union[StreamOptions, dict[str, Any]]] = None,
) -> AsyncIterable[ChatCompletionChunk]:
    """
    Generate streaming chat completion.

    Args:
        provider: LLM provider ("openai", "anthropic", or "google")
        api_key: API key for the provider
        model: Model identifier (provider-specific)
        messages: Conversation history or list of message dicts
        tools: Optional list of tool/function definitions
        tool_choice: Tool choice strategy ("none", "auto", "required", or tool name)
        temperature: Sampling temperature (0.0-2.0)
        timeout: Request timeout in seconds
        max_tokens: Maximum tokens to generate
        stream_options: TODO

    Returns:
        AsyncIterable of ChatCompletionChunk objects (typed chunks)
    """

    # Normalize string input to enum
    if isinstance(provider, str):
        try:
            provider = CompletionsProvider(provider.lower())
        except ValueError:
            raise ValueError(f"Invalid provider: {provider}.")

    # Normalize messages to proper message objects
    normalized_messages = normalize_messages(messages)

    # Normalize tools to proper tool objects
    normalized_tools = normalize_tools(tools) if tools else None

    # Normalize stream options if provided as dict
    if stream_options and isinstance(stream_options, dict):
        stream_options = StreamOptions.deserialize(stream_options)

    client: CompletionClient
    if provider == CompletionsProvider.OPENAI:
        client = OpenAiCompletionClient()
    elif provider == CompletionsProvider.ANTHROPIC:
        client = AnthropicCompletionClient()
    elif provider == CompletionsProvider.GOOGLE:
        # TODO: enable once google fixes their SDK
        raise ValueError(f"Google streaming currently unsupported")
        # client = GoogleCompletionClient()
    else:
        raise ValueError(f"Invalid provider: {provider}")

    request = ChatCompletionRequest(
        provider=provider,
        api_key=api_key,
        model=model,
        messages=normalized_messages,
        tools=normalized_tools,
        tool_choice=tool_choice,
        temperature=temperature,
        timeout=timeout,
        max_tokens=max_tokens,
        streaming=True,
        stream_options=stream_options,
    )

    return client.generate_chat_completion_stream(request=request)

