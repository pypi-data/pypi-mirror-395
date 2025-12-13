import base64
from typing import AsyncIterator, List, Any
from google import genai
from google.genai import types

from dragonglass.core.config import settings
from dragonglass.core.models import Message, CompletionConfig, ContentPart, Role, MediaType
from dragonglass.core.protocols import LLMProvider
from dragonglass.utils import console

# Map our internal safety settings to genai's
SAFETY_SETTINGS_MAP = {
    "BLOCK_NONE": [
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=types.HarmBlockThreshold.BLOCK_NONE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_NONE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=types.HarmBlockThreshold.BLOCK_NONE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=types.HarmBlockThreshold.BLOCK_NONE,
        ),
    ],
    "HARM_ONLY": [
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
    ],
}


class GeminiProvider(LLMProvider):
    """Gemini API implementation of the LLMProvider protocol using the new Google Gen AI SDK."""

    def __init__(self):
        api_key = settings.gemini.api_key
        if not api_key:
            console.print(
                "Gemini API key not found. Set the GOOGLE_API_KEY environment "
                "variable or configure it in ~/.config/dg/config.toml"
            )
            raise ValueError("Gemini API key not configured.")

        self.client = genai.Client(
            api_key=api_key

        )

    @property
    def id(self) -> str:
        return "gemini"

    def _to_genai_content(self, messages: List[Message]) -> List[types.Content]:
        genai_contents: List[types.Content] = []
        for msg in messages:
            parts: List[types.Part] = []
            for part in msg.parts:
                if part.type == MediaType.TEXT:
                    parts.append(types.Part(text=part.data))
                elif part.type.startswith("image/"):
                    try:
                        image_bytes = base64.b64decode(part.data)
                        parts.append(types.Part(inline_data=types.Blob(mime_type=part.type, data=image_bytes)))
                    except Exception as e:
                        console.print(f"Failed to decode base64 image data for part: {e}")
                        continue

            role = "user" if msg.role == Role.USER else "model"
            genai_contents.append(types.Content(role=role, parts=parts))
        return genai_contents

    def _to_dg_message(self, text: str, role: Role = Role.MODEL) -> Message:
        return Message(role=role, parts=[ContentPart(type=MediaType.TEXT, data=text)])


    async def stream_chat(self,
            messages: List[Message],
            config: CompletionConfig
        ) -> AsyncIterator[str]:
        
        contents = self._to_genai_content(messages)

        gen_config = types.GenerateContentConfig(
            temperature=config.temperature,
            max_output_tokens=config.max_tokens,
            top_p=config.top_p,
            stop_sequences=config.stop_sequences,
            response_mime_type=config.response_mime_type,
            safety_settings=SAFETY_SETTINGS_MAP.get(settings.gemini.safety_settings, SAFETY_SETTINGS_MAP["HARM_ONLY"])
        )

        try:


            async for chunk in await self.client.aio.models.generate_content_stream(
                    model=config.model,
                    contents=contents,
                    config=gen_config,
            ):
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            console.print(f"Gemini stream error: {e}")
            raise

    async def complete_chat(
            self,
            messages: List[Message],
            config: CompletionConfig
    ) -> Message:

        contents = self._to_genai_content(messages)

        gen_config = types.GenerateContentConfig(
            temperature=config.temperature,
            max_output_tokens=config.max_tokens,
            top_p=config.top_p,
            stop_sequences=config.stop_sequences,
            response_mime_type=config.response_mime_type,
            safety_settings=SAFETY_SETTINGS_MAP.get(settings.gemini.safety_settings, SAFETY_SETTINGS_MAP["HARM_ONLY"])
        )

        try:
            response = await self.client.aio.models.generate_content(
                model=config.model,
                contents=contents,
                config=gen_config,
            )
            return self._to_dg_message(response.text or "", Role.MODEL)
        except Exception as e:
            console.print(f"Gemini completion error: {e}")
            raise

    async def embed_text(self, text: str) -> List[float]:
        """Generates an embedding vector for the given text using text-embedding-004."""
        try:
            response = await self.client.aio.models.embed_content(
                model="gemini-embedding-001",
                contents=text,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT"
                )
            )
            # Response structure: EmbedContentResponse(embeddings=[ContentEmbedding(values=[...])])
            if response.embeddings and response.embeddings[0].values:
                return response.embeddings[0].values
            return []
        except Exception as e:
            console.print(f"Gemini embedding error: {e}")
            raise
