from typing import  Any, AsyncIterable, Dict, List, Optional
from openai.types.chat.chat_completion_chunk import (
    Choice as OpenAiChunkChoice,
    ChoiceDelta as OpenAiChoiceDelta,
    ChatCompletionChunk as OpenAiCompletionChunk,
    ChoiceDeltaToolCall as OpenAiToolDelta,
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


class OpenAiStreamProcessor(StreamProcessor):
    """Processes OpenAI chat completion stream yielding normalized chunks."""


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

        self.active_calls: Dict[int, PartialToolCall] = {}
        self.content: str = ""
        self.tool_calls: List[ToolCall] = []
        self.finish_reason: str = ""
        self.usage: Dict[str, Any] = {}
        self.sentence_buffer = ""


    def _process_tool_deltas(self, tool_call_deltas: List[OpenAiToolDelta]) -> List[ToolCallChunk]:
        """Process a tool call delta and return any completed tool call chunks."""
        chunks: List[ToolCall] = []

        for delta in tool_call_deltas:
            # Tool call already in buffer
            if delta.index in self.active_calls:
                partial_call = self.active_calls[delta.index]
                if delta.function and delta.function.arguments:
                    partial_call.arguments_buffer += delta.function.arguments

                    # Check if tool call complete
                    if partial_call.is_complete():
                        # Complete tool call, remove from active calls and return
                        completed_call = partial_call.to_tool_call()
                        del self.active_calls[delta.index]

                        # Append full tool call to chunks to stream
                        chunks.append(ToolCallChunk(
                            tool_call=completed_call
                        ))

                        # Add tool call to accumulated response
                        self.tool_calls.append(completed_call)

            # New tool call
            else:
                self.active_calls[delta.index] = PartialToolCall(
                    id=delta.id,
                    type=delta.type,
                    function_name=delta.function.name,
                    arguments_buffer=delta.function.arguments or "",
                    index=delta.index,
                )

        return chunks


    def _process_chunk(
        self,
        chunk: OpenAiCompletionChunk,
    ) -> List[ChatCompletionChunk]:
        """Convert OpenAI ChatCompletionChunk to individual typed chunks."""
        chunks = []

        # Handle usage chunk
        if chunk.usage:
            self.usage = chunk.usage.model_dump()

        # Handle no choices
        if not chunk.choices:
            return chunks

        # Take only first choice (OpenAI pattern)
        choice: OpenAiChunkChoice = chunk.choices[0]
        delta: OpenAiChoiceDelta = choice.delta

        # Handle content
        if delta.content:
            if self.stream_sentences:
                # Append delta to sentence buffer
                sentence_buffer, complete_sentence = update_sentence_buffer(
                    content=delta.content,
                    sentence_buffer=self.sentence_buffer,
                    punctuation_marks=self.punctuation_marks,
                    clean_text=self.clean_sentences,
                    # TODO: this completely drops messages like "Sure."
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
                    content=delta.content
                ))

            # Add content delta to accumulated response
            self.content += delta.content

        # Handle tool calls
        if delta.tool_calls:
            chunks.extend(self._process_tool_deltas(delta.tool_calls))

        # Capture finish reason
        if choice.finish_reason:
            self.finish_reason = choice.finish_reason

        return chunks
    
    async def process_stream(
        self,
        stream: AsyncIterable[OpenAiCompletionChunk],
    ) -> AsyncIterable[ChatCompletionChunk]:
        async for chunk in stream:
            for normalized_chunk in self._process_chunk(chunk):
                yield normalized_chunk

        if self.stream_sentences and self.sentence_buffer:
            # Clean text for speech if requested
            complete_sentence = clean_text_for_speech(self.sentence_buffer) if self.clean_sentences else self.sentence_buffer
            # Handle any remaining text in sentence buffer
            yield AssistantMessageSentenceChunk(
                sentence=complete_sentence
            )

        # Yield the finish chunk (or default)
        yield FinishReasonChunk(finish_reason=self.finish_reason or "stop")

        # Yield the usage chunk
        yield UsageChunk(usage=self.usage)

        # Yield aggregated chat completion response as final chunk
        yield FinalResponseChunk(
            response = ChatCompletionResponse(
                message=AssistantMessage(
                    content=self.content or None,
                    tool_calls=self.tool_calls or None
                ),
                usage=self.usage,
                finish_reason=self.finish_reason,
            )
        )