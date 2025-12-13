from typing import Protocol, AsyncIterator, List, runtime_checkable
from dragonglass.core.models import Message, CompletionConfig


@runtime_checkable
class LLMProvider(Protocol):
    """Interface for any model backend."""

    @property
    def id(self) -> str: ...

    def stream_chat(
        self, messages: list[Message], config: CompletionConfig
    ) -> AsyncIterator[str]:
        """Yields chunks of generated text."""
        ...

    async def complete_chat(
        self, messages: list[Message], config: CompletionConfig
    ) -> Message:
        """Returns the complete response message."""
        ...

    async def embed_text(self, text: str) -> List[float]:
        """Generates an embedding vector for the given text."""
        ...
