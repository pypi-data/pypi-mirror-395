from typing import Optional
from google.genai.types import (
    Content as GoogleMessageContent,
    Part as GoogleMessagePart,
    FunctionDeclaration as GoogleFunctionDefinition,
    Tool as GoogleToolDefinition,
    ToolConfig as GoogleToolChoice,
    FunctionCallingConfig as GoogleFunctionChoice,
)
from primfunctions.completions.messages import (
    ConversationHistory,
    UserMessage,
    AssistantMessage,
    SystemMessage,
    ToolResultMessage,
)
from primfunctions.completions.request import ToolChoice, ToolDefinition


def denormalize_conversation_history(normalized_messages: ConversationHistory) -> tuple[list[GoogleMessageContent], Optional[str]]:
    """Convert normalized Message objects to Google Content format.

    Returns:
        Tuple of (contents, system_instruction) since Google handles system prompts separately
    """
    contents: list[GoogleMessageContent] = []
    system_messages: list[str] = []

    # TODO: thought signatures required https://ai.google.dev/gemini-api/docs/thought-signatures skip_thought_signature_validator?

    for msg in normalized_messages:
        match msg:
            case SystemMessage():
                system_messages.append(msg.content)
            case UserMessage():
                parts = []
                if msg.content:
                    parts.append(GoogleMessagePart.from_text(text=msg.content))

                content = GoogleMessageContent(
                    role="user",
                    parts=parts
                )
                contents.append(content)
            case AssistantMessage():
                # Assistant messages (model role in Google)
                parts = []

                # Add text content if present
                if msg.content:
                    parts.append(GoogleMessagePart.from_text(text=msg.content))

                # Add function calls if present
                if msg.tool_calls:
                    for tc in msg.tool_calls:
                        # function_call = GoogleFunctionCall(
                        #     id=tc.id,
                        #     name=tc.function.name,
                        #     args=tc.function.arguments
                        # )
                        parts.append(GoogleMessagePart.from_function_call(
                            name=tc.function.name,
                            args=tc.function.arguments
                        ))

                content = GoogleMessageContent(
                    role="model",
                    parts=parts
                )
                contents.append(content)
            case ToolResultMessage():
                # Tool results become function_response parts in user messages
                # Need to find the corresponding function name from tool_call_id
                # For now, we'll need to track function names separately or get from context
                if msg.tool_call_id and msg.content:
                    # TODO: We need the function name from the original tool call
                    # This requires tracking the function name when processing assistant messages
                    # function_response = GoogleFunctionResponse(
                    #     id=msg.tool_call_id,
                    #     name=msg.name or "unknown_function",  # Name is required
                    #     response={"output": msg.content}
                    # )

                    content = GoogleMessageContent(
                        role="user",
                        parts=[GoogleMessagePart.from_function_response(
                            name=msg.name or "unknown_function",
                            response={"output": msg.content}
                        )]
                    )
                    contents.append(content)

    # Combine system messages with newlines
    system_instruction: Optional[str] = "\n".join(system_messages) if system_messages else None

    return contents, system_instruction


def denormalize_tools(normalized_tools: Optional[list[ToolDefinition]]) -> Optional[list[GoogleToolDefinition]]:
    """Convert normalized Tool objects to Google Tool format."""

    function_defs: Optional[list[GoogleFunctionDefinition]] = None
    if normalized_tools:
        function_defs = []
        for tool in normalized_tools:
            function_declaration = GoogleFunctionDefinition(
                name=tool.function.name,
                description=tool.function.description,
                parameters=tool.function.parameters
            )
            function_defs.append(function_declaration)

    # All google function calling tools are included in a single Google Tool
    return [GoogleToolDefinition(function_declarations=function_defs)] if function_defs else None


def denormalize_tool_choice(normalized_tool_choice: Optional[ToolChoice]) -> Optional[GoogleToolChoice]:
    """Convert normalized ToolChoice to Google GoogleToolChoice format."""
    if not normalized_tool_choice:
        return None

    # Google uses ToolConfig with FunctionCallingConfig
    if normalized_tool_choice == "auto":
        return GoogleToolChoice(
            function_calling_config=GoogleFunctionChoice(mode="AUTO")
        )
    elif normalized_tool_choice == "none":
        return GoogleToolChoice(
            function_calling_config=GoogleFunctionChoice(mode="NONE")
        )
    elif normalized_tool_choice == "required":
        return GoogleToolChoice(
            function_calling_config=GoogleFunctionChoice(mode="ANY")
        )
    else:
        # Specific tool name - use allowed_function_names
        return GoogleToolChoice(
            function_calling_config=GoogleFunctionChoice(
                mode="ANY",
                allowed_function_names=[normalized_tool_choice]
            )
        )
