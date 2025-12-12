from typing import Any, AsyncIterable, Dict, List, Optional
from anthropic.types import (
    RawMessageStreamEvent as AnthropicStreamEvent,
    RawMessageStartEvent as AnthropicMessageStartEvent,
    RawContentBlockStartEvent as AnthropicStartEvent,
    RawContentBlockDeltaEvent as AnthropicContentDeltaEvent,
    RawMessageDeltaEvent as AnthropicMessageDeltaEvent,
    TextDelta as AnthropicTextDelta,
    InputJSONDelta as AnthropicJsonDelta,
    ToolUseBlock as AnthropicToolCall,
    TextBlock as AnthropicTextBlock,
)
from primfunctions.completions.messages import ToolCall, AssistantMessage
from primfunctions.completions.response import ChatCompletionResponse
from primfunctions.completions.streaming import (
    ChatCompletionChunk,
    AssistantMessageDeltaChunk,
    AssistantMessageSentenceChunk,
    FinishReasonChunk,
    ToolCallChunk,
    UsageChunk,
    FinalResponseChunk,
)
from primfunctions.utils.streaming import update_sentence_buffer, clean_text_for_speech
from primfunctions.completions.request import StreamOptions

from ..base import StreamProcessor, PartialToolCall


class AnthropicStreamProcessor(StreamProcessor):
    """Processes Anthropic message stream events yielding normalized chunks."""

    def __init__(
        self,
        stream_options: Optional[StreamOptions] = None,
    ):
        self.stream_sentences: bool = False
        self.clean_sentences: bool = True
        self.min_sentence_length: int = 6
        self.punctuation_marks: Optional[list[str]] = None
        self.punctuation_language: Optional[str] = None

        # Override stream options defaults
        if stream_options:
            self.stream_sentences = stream_options.stream_sentences
            self.clean_sentences = stream_options.clean_sentences
            self.min_sentence_length = stream_options.min_sentence_length
            self.punctuation_marks = stream_options.punctuation_marks
            self.punctuation_language = stream_options.punctuation_language

        self.active_call: PartialToolCall = None
        self.active_call_index = 0
        self.content: str = ""
        self.tool_calls: List[ToolCall] = []
        self.finish_reason: str = ""
        self.usage: Dict[str, Any] = {}
        self.sentence_buffer = ""

    
    def _process_text_partial(self, text: str) -> List[ChatCompletionChunk]:
        """Process text partial."""
        chunks: List[ChatCompletionChunk] = []

        if not text:
            return chunks

        if self.stream_sentences:
            # Append delta to sentence buffer
            sentence_buffer, complete_sentence = update_sentence_buffer(
                content=text,
                sentence_buffer=self.sentence_buffer,
                punctuation_marks=self.punctuation_marks,
                clean_text=self.clean_sentences,
                min_sentence_length=self.min_sentence_length,
            )
            self.sentence_buffer = sentence_buffer

            if complete_sentence:
                chunks.append(AssistantMessageSentenceChunk(
                    sentence=complete_sentence
                ))
        else:
            # Otherwise stream content delta directly
            chunks.append(AssistantMessageDeltaChunk(
                content=text
            ))

        # Add content delta to accumulated response
        self.content += text

        return chunks


    def _process_event(
        self,
        event: AnthropicStreamEvent,
    ) -> List[ChatCompletionChunk]:
        """Convert Anthropic streaming event to individual typed chunks."""
        chunks = []

        match event.type:
            case "message_start":
                msg_start_event: AnthropicMessageStartEvent = event

                # Capture usage from message start
                self.usage.update(msg_start_event.message.usage.model_dump())

            case "content_block_start":
                start_event: AnthropicStartEvent = event
                
                # For tool_use blocks, initialize the partial tool call
                if start_event.content_block.type == "tool_use":
                    tool_block: AnthropicToolCall = start_event.content_block
                    self.active_call = PartialToolCall(
                        id=tool_block.id,
                        type="function",
                        function_name=tool_block.name,
                        arguments_buffer="",
                        index=self.active_call_index,
                    )
                elif start_event.content_block.type == "text":
                    text_block: AnthropicTextBlock = start_event.content_block
                    chunks.extend(self._process_text_partial(text_block.text))

            case "content_block_delta":
                delta_event: AnthropicContentDeltaEvent = event

                if hasattr(delta_event.delta, 'type'):
                    # Handle text content delta
                    if delta_event.delta.type == "text_delta":
                        text_delta: AnthropicTextDelta = delta_event.delta
                        chunks.extend(self._process_text_partial(text_delta.text))

                    # Handle JSON content delta
                    if delta_event.delta.type == "input_json_delta" and self.active_call:
                        json_delta: AnthropicJsonDelta = delta_event.delta
                        self.active_call.arguments_buffer += json_delta.partial_json

            case "content_block_stop":
                # Only special handling for tool call
                if self.active_call:
                    tool_call = self.active_call.to_tool_call()
                    chunks.append(ToolCallChunk(tool_call=tool_call))
                    self.tool_calls.append(tool_call)
                    self.active_call = None
                    self.active_call_index += 1

            case "message_delta":
                msg_delta_event: AnthropicMessageDeltaEvent = event

                # Handle usage information if present
                if msg_delta_event.usage:
                    self.usage.update(msg_delta_event.usage.model_dump())

                # Handle finish reason from delta
                if msg_delta_event.delta.stop_reason:
                    self.finish_reason = msg_delta_event.delta.stop_reason

            case "message_stop":
                # End of message - no special handling
                pass

        return chunks

    async def process_stream(
        self,
        stream: AsyncIterable[AnthropicStreamEvent],
    ) -> AsyncIterable[ChatCompletionChunk]:
        """Process Anthropic event stream and yield normalized chunks."""
        async for event in stream:
            for chunk in self._process_event(event):
                yield chunk

        # Handle remaining sentence buffer if streaming sentences
        if self.stream_sentences and self.sentence_buffer:
            complete_sentence = clean_text_for_speech(self.sentence_buffer) if self.clean_sentences else self.sentence_buffer
            yield AssistantMessageSentenceChunk(
                sentence=complete_sentence
            )

        # Yield the finish chunk (or default)
        yield FinishReasonChunk(finish_reason=self.finish_reason or "stop")

        # Yield the usage chunk
        yield UsageChunk(usage=self.usage)

        # Yield aggregated chat completion response as final chunk
        yield FinalResponseChunk(
            response=ChatCompletionResponse(
                message=AssistantMessage(
                    content=self.content or None,
                    tool_calls=self.tool_calls or None,
                ),
                usage=self.usage,
                finish_reason=self.finish_reason,
            )
        )