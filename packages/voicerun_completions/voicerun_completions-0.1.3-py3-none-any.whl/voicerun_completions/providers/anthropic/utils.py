import json
from typing import Optional, List, Union
from anthropic.types import (
    MessageParam as AnthropicMessage,
    ToolParam as AnthropicToolDefinition,
    ToolChoiceParam as AnthropicToolChoice,
    ContentBlock as AnthropicContentBlock,
    TextBlockParam as AnthropicTextBlock,
    ToolUseBlockParam as AnthropicToolCall,
    ToolResultBlockParam as AnthropicToolResult,
    ToolChoiceAutoParam as AnthropicToolChoiceAuto,
    ToolChoiceAnyParam as AnthropicToolChoiceAny,
    ToolChoiceNoneParam as AnthropicToolChoiceNone,
    ToolChoiceToolParam as AnthropicToolChoiceToolName,
    CacheControlEphemeralParam as AnthropicCacheControl,
)
from primfunctions.completions.messages import (
  ConversationHistory,
  UserMessage,
  AssistantMessage,
  SystemMessage,
  ToolResultMessage,
  ToolCall,
)
from primfunctions.completions.request import ToolChoice, ToolDefinition


def denormalize_tool_calls(normalized_tool_calls: Optional[List[ToolCall]]) -> list[AnthropicToolCall]:
    """TODO"""

    tool_calls: Optional[list[AnthropicToolCall]] = None
    if normalized_tool_calls:
        tool_calls = []
        for tc in normalized_tool_calls:
            tool_call: AnthropicToolCall = {
                "type": "tool_use",
                "id": tc.id,
                "name": tc.function.name,
                "input": tc.function.arguments,
            }
            tool_calls.append(tool_call)

    return tool_calls


def denormalize_conversation_history(normalized_messages: ConversationHistory) -> tuple[list[AnthropicMessage], Optional[list[AnthropicTextBlock]]]:
    """Convert normalized Message objects to Anthropic MessageParam format.

    Returns:
        Tuple of (messages, system_prompt) since Anthropic handles system prompts separately
    """

    messages: list[AnthropicMessage] = []
    system_messages: list[AnthropicTextBlock] = []

    i = 0
    while i < len(normalized_messages):
        msg = normalized_messages[i]

        match msg:
            case UserMessage():
                # User messages: simple content handling
                user_message: AnthropicMessage = {
                    "role": "user",
                    "content": [
                        AnthropicTextBlock(
                            type="text",
                            text=msg.content or "",
                            cache_control=AnthropicCacheControl(
                                type="ephemeral",
                                ttl=msg.cache_breakpoint.ttl,
                            ) if msg.cache_breakpoint else None
                        )
                    ],
                }
                messages.append(user_message)
                i += 1
            case AssistantMessage():
                # Build content blocks
                content_blocks: list[AnthropicContentBlock] = []

                # Add text content if present
                if msg.content:
                    content_blocks.append(AnthropicTextBlock(
                        type="text",
                        text=msg.content,
                    ))

                # Add tool calls
                if msg.tool_calls:
                    tool_calls = denormalize_tool_calls(msg.tool_calls)
                    if tool_calls:
                        content_blocks.extend(tool_calls)

                # Capture cache control of assistant message
                cache_control = AnthropicCacheControl(
                    type="ephemeral",
                    ttl=msg.cache_breakpoint.ttl,
                ) if msg.cache_breakpoint else None

                # Add cache control to final block if present and blocks exist
                if cache_control and content_blocks:
                    final_block: Union[AnthropicTextBlock, AnthropicToolCall] = content_blocks[-1]
                    final_block["cache_control"] = cache_control

                assistant_message: AnthropicMessage = {
                    "role": "assistant",
                    "content": content_blocks
                }

                messages.append(assistant_message)
                i += 1
            case SystemMessage():
                # Collect all system and developer messages
                system_messages.append(
                    AnthropicTextBlock(
                        type="text",
                        text=msg.content or "",
                        cache_control=AnthropicCacheControl(
                            type="ephemeral",
                            ttl=msg.cache_breakpoint.ttl,
                        ) if msg.cache_breakpoint else None
                    )
                )
                i += 1
            case ToolResultMessage():
                # Look ahead to group consecutive tool messages into a single user message
                tool_results: list[AnthropicToolResult] = []
                while i < len(normalized_messages) and normalized_messages[i].role == "tool":
                    tool_msg: ToolResultMessage = normalized_messages[i]
                    tool_results.append(AnthropicToolResult(
                        type="tool_result",
                        tool_use_id=tool_msg.tool_call_id,
                        content=json.dumps(tool_msg.content),
                        cache_control=AnthropicCacheControl(
                            type="ephemeral",
                            ttl=tool_msg.cache_breakpoint.ttl,
                        ) if tool_msg.cache_breakpoint else None
                    ))
                    i += 1

                # Create user message with all tool results
                user_message: AnthropicMessage = {
                    "role": "user",
                    "content": tool_results
                }
                messages.append(user_message)
            case _:
                # Skip unsupported roles
                i += 1

    # Capture system prompt as list of TextBlocks
    system_prompt: list[AnthropicTextBlock] = system_messages or None

    return messages, system_prompt


def denormalize_tools(normalized_tools: Optional[list[ToolDefinition]]) -> Optional[list[AnthropicToolDefinition]]:
    """Convert normalized Tool objects to Anthropic ToolParam format."""

    tools: Optional[list[AnthropicToolDefinition]] = None
    if normalized_tools:
        tools = []
        for tool in normalized_tools:
            tool_def: AnthropicToolDefinition = {
                "name": tool.function.name,
                "description": tool.function.description,
                "input_schema": tool.function.parameters,
                "cache_control": AnthropicCacheControl(
                    type="ephemeral",
                    ttl=tool.cache_breakpoint.ttl,
                ) if tool.cache_breakpoint else None
            }
            tools.append(tool_def)

    return tools


def denormalize_tool_choice(normalized_tool_choice: Optional[ToolChoice]) -> Optional[AnthropicToolChoice]:
    """Convert normalized ToolChoice to Anthropic ToolChoiceParam format."""

    if not normalized_tool_choice:
        return None

    # Map our normalized tool choice to Anthropic's format using proper SDK types
    if normalized_tool_choice == "auto":
        return AnthropicToolChoiceAuto(type="auto")
    elif normalized_tool_choice == "none":
        return AnthropicToolChoiceNone(type="none")
    elif normalized_tool_choice == "required":
        return AnthropicToolChoiceAny(type="any")  # Anthropic uses "any" for required
    else:
        # Specific tool name - use ToolChoiceToolParam
        return AnthropicToolChoiceToolName(
            type="tool",
            name=normalized_tool_choice
        )
