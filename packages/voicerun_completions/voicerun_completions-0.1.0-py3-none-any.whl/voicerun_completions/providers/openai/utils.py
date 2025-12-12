import json
from typing import List, Optional
from openai.types.chat import (
    ChatCompletionToolChoiceOptionParam as OpenAiToolChoice,
    ChatCompletionNamedToolChoiceParam as OpenAiNamedToolChoice,
    ChatCompletionFunctionToolParam as OpenAiToolDefinition,
    ChatCompletionMessageParam as OpenAiMessage,
    ChatCompletionUserMessageParam as OpenAiUserMessage,
    ChatCompletionAssistantMessageParam as OpenAiAssistantMessage,
    ChatCompletionSystemMessageParam as OpenAiSystemMessage,
    ChatCompletionToolMessageParam as OpenAiToolResultMessage,
    ChatCompletionMessageFunctionToolCallParam as OpenAiToolCall,
)
from openai.types.shared_params import FunctionDefinition as OpenAiFunctionDefinition
from openai.types.chat.chat_completion_message_function_tool_call_param import Function as OpenAiFunctionCall
from primfunctions.completions.messages import (
    ConversationHistory,
    UserMessage,
    AssistantMessage,
    SystemMessage,
    ToolResultMessage,
    ToolCall,
    FunctionCall,
)
from primfunctions.completions.request import ToolChoice, ToolDefinition


def denormalize_tool_calls(normalized_tool_calls: Optional[List[ToolCall]]) -> list[OpenAiToolCall]:
    """TODO"""
    tool_calls: Optional[list[OpenAiToolCall]] = None
    if normalized_tool_calls:
        tool_calls = []
        for tc in normalized_tool_calls:
            function_call: OpenAiFunctionCall = {
                "name": tc.function.name,
                "arguments": json.dumps(tc.function.arguments),
            }
            tool_call: OpenAiToolCall = {
                "id": tc.id,
                "type": tc.type,
                "function": function_call
            }
            tool_calls.append(tool_call)

    return tool_calls


def denormalize_conversation_history(normalized_messages: ConversationHistory) -> list[OpenAiMessage]:
    # Convert conversation history to ChatCompletionMessageParams
    messages: list[OpenAiMessage] = []
    for msg in normalized_messages:
        match msg:
            case UserMessage():
                messages.append(OpenAiUserMessage(
                    role="user",
                    content=msg.content,
                ))
            case AssistantMessage():
                messages.append(OpenAiAssistantMessage(
                    role="assistant",
                    content=msg.content,
                    tool_calls=denormalize_tool_calls(msg.tool_calls),
                ))
            case SystemMessage():
                messages.append(OpenAiSystemMessage(
                    role="system",
                    content=msg.content,
                ))
            case ToolResultMessage():
                tool_result: OpenAiToolResultMessage = {
                    "role": "tool",
                    "content": json.dumps(msg.content),
                    "tool_call_id": msg.tool_call_id,
                }
                messages.append(tool_result)

    return messages


def denormalize_tools(normalized_tools: Optional[list[ToolDefinition]]) -> Optional[list[OpenAiToolDefinition]]:
    # Convert tools to ChatCompletionFunctionToolParam format if provided
    tools: Optional[list[OpenAiToolDefinition]] = None
    if normalized_tools:
        tools = []
        for tool in normalized_tools:
            function_def: OpenAiFunctionDefinition = {
                "name": tool.function.name,
                "description": tool.function.description,
                "parameters": tool.function.parameters,
                "strict": tool.function.strict,
            }
            tool_def: OpenAiToolDefinition = {
                "type": tool.type,
                "function": function_def,
            }
            tools.append(tool_def)

    return tools


def denormalize_tool_choice(normalized_tool_choice: Optional[ToolChoice]) -> Optional[OpenAiToolChoice]:
    """Convert normalized ToolChoice to OpenAI ChatCompletionToolChoiceOptionParam format."""
    tool_choice: Optional[OpenAiToolChoice] = None
    if normalized_tool_choice:
        # Handle literal values that are directly compatible
        if normalized_tool_choice in ["none", "auto", "required"]:
            tool_choice = normalized_tool_choice
        else:
            # TODO: support ChatCompletionNamedToolChoiceCustomParam
            # Assume tool name
            tool_choice = OpenAiNamedToolChoice(
                type="function",
                function={"name": normalized_tool_choice}
            )

    return tool_choice


def normalize_tool_calls(denormalized_tool_calls: Optional[List[OpenAiToolCall]]) -> list[ToolCall]:
    """Convert denormalized ChatCompletionMessageFunctionToolCallParam to ToolCall format."""
    tool_calls: Optional[list[ToolCall]] = None
    if denormalized_tool_calls:
        tool_calls = []
        for index, tc in enumerate(denormalized_tool_calls):
            tool_calls.append(ToolCall(
                id=tc.id,
                type=tc.type,
                function=FunctionCall(
                    name=tc.function.name,
                    arguments=json.loads(tc.function.arguments)
                ),
                index=index,
            ))

    return tool_calls
