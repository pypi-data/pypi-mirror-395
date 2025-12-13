from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Dict, Any, List


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    MODEL = "model"  # Gemini convention
    TOOL = "tool"  # For future tool use


class MediaType(str, Enum):
    TEXT = "text/plain"
    IMAGE_PNG = "image/png"
    IMAGE_JPEG = "image/jpeg"
    # Add other media types as needed, e.g., audio/mpeg


class ContentPart(BaseModel):
    """A single part of a multimodal message."""

    type: MediaType
    data: str  # Text content or Base64 encoded binary
    source_uri: str | None = (
        None  # For tracking file origins (e.g., file://path/to/image.png)
    )

    model_config = ConfigDict(frozen=True)


class Message(BaseModel):
    """Immutable multimodal message entity."""

    role: Role
    parts: List[ContentPart]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(frozen=True)


class CompletionConfig(BaseModel):
    """Runtime configuration for a generation request."""

    model: str
    temperature: float = Field(0.7, ge=0.0, le=1.0)
    max_tokens: int | None = Field(6080, ge=1)
    top_p: float = Field(1.0, ge=0.0, le=1.0)
    stop_sequences: List[str] = Field(default_factory=list)
    stream: bool = True

    # Gemini-specific response format
    response_mime_type: Literal["text/plain", "application/json"] = "text/plain"
