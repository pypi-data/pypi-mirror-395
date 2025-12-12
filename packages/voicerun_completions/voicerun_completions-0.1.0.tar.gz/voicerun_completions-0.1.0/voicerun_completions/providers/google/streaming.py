import httpx
from typing import Any, AsyncIterable, Dict, List, Optional
from google.genai.types import (
    Candidate as GoogleResponseCandidate,
    GenerateContentResponse as GoogleResponseChunk,
    Content as GoogleMessageContent,
    Part as GoogleMessagePart,
)
from primfunctions.completions.messages import ToolCall, FunctionCall, AssistantMessage
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


class GoogleStreamProcessor(StreamProcessor):
    """Processes Google message stream events yielding normalized chunks."""

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
        self.current_block_index = 0


    def _process_chunk(
        self,
        chunk: GoogleResponseChunk,
    ) -> List[ChatCompletionChunk]:
        """Convert Google ContentResponse to individual typed chunks."""
        chunks = []

        # Handle usage information
        if chunk.usage_metadata:
            # TODO: ensure cumulative
            self.usage = chunk.usage_metadata.model_dump()

        # Handle candidates
        if not chunk.candidates:
            return chunks

        # Take only first candidate (Google pattern)
        candidate: GoogleResponseCandidate = chunk.candidates[0]
        content: GoogleMessageContent = candidate.content
        parts: list[GoogleMessagePart] = content.parts

        # Handle finish reason
        if candidate.finish_reason:
            self.finish_reason = candidate.finish_reason.value.lower()

        # Process each part in the content
        for part in parts:
            # Handle text content
            if part.text:
                chunks.extend(self._process_text_partial(part.text))

            # Handle function calls (tool calls)
            elif part.function_call:
                # Google returns complete function calls, not deltas
                tool_call = ToolCall(
                    id=part.function_call.id or f"call_{self.current_block_index}",
                    type="function",
                    function=FunctionCall(
                        name=part.function_call.name,
                        arguments=part.function_call.args,
                    ),
                    index=self.current_block_index,
                )

                chunks.append(ToolCallChunk(tool_call=tool_call))
                self.tool_calls.append(tool_call)
                self.current_block_index += 1

        return chunks

    def _process_text_partial(self, text: str) -> List[ChatCompletionChunk]:
        """Process text content and return appropriate chunks."""
        chunks = []

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

    async def process_stream(
        self,
        stream: AsyncIterable[GoogleResponseChunk],
    ) -> AsyncIterable[ChatCompletionChunk]:
        """Process Google event stream and yield normalized chunks."""
        try:
            async for event in stream:
                for chunk in self._process_chunk(event):
                    yield chunk
        except Exception as e:
            # Handle Google API connection issues that occur after successful content delivery
            if isinstance(e, httpx.ReadError) and str(e) == '':
                # This is a known issue with Google's streaming API - ignore empty ReadErrors
                # that occur after content has been successfully delivered
                pass
            else:
                raise

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
