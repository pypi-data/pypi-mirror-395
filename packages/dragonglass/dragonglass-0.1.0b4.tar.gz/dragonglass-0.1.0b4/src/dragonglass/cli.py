import sys
import base64
import asyncio

import typer

from pathlib import Path
from typing import List, Optional
from typing_extensions import Annotated

from dragonglass.core.config import settings
from dragonglass.core.models import (
    CompletionConfig,
    ContentPart,
    MediaType,
    Message,
    Role,
)
from dragonglass.core.rag import VectorSearch
from dragonglass.infra.db import db
from dragonglass.infra.providers.gemini import GeminiProvider
from dragonglass.utils import Markdown, console


def _read_stdin() -> str | None:
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None


def _ensure_api_key():
    """Validates that the API key is present before running commands that require it."""
    if not settings.gemini.api_key:
        console.print(
            """
        [bold red]Error: Gemini API key not found.[/bold red]
        
        Please set the [bold]DG_GEMINI__API_KEY[/bold] environment variable 
        or configure it in [bold]~/.config/dg/config.toml[/bold]:

        [dim]
        # config.toml
            [gemini]
            google_api_key="A....D2E"
            default_model="gemini-3-pro-preview"
            temperature=0.7
            top_p=1.0
            safe_settings="BLOCK_NONE"
            grounding_enabled=true
        [/dim]
        """
        )
        sys.exit(1)


def _detect_media_type(path: Path) -> MediaType:
    suffix = path.suffix.lower()
    if suffix == ".png":
        return MediaType.IMAGE_PNG
    if suffix in (".jpg", ".jpeg"):
        return MediaType.IMAGE_JPEG
    return MediaType.TEXT


def _build_inputs(
    prompt: str, images: List[Path], files: List[Path]
) -> List[ContentPart]:

    parts = []
    if stdin_content := _read_stdin():
        parts.append(
            ContentPart(type=MediaType.TEXT, data=f"Context:\n{stdin_content}")
        )

        # 2. Files
    for f in files:
        try:
            parts.append(
                ContentPart(
                    type=MediaType.TEXT,
                    data=f"File {f.name}:\n{f.read_text()}",
                    source_uri=f"file://{f.absolute()}",
                )
            )
        except Exception as e:
            console.print(f"Error reading {f.name}: {e}")

            # 3. Images
    for img in images:
        try:
            mime = _detect_media_type(img)
            if not mime.startswith("image/"):
                continue
            b64_data = base64.b64encode(img.read_bytes()).decode("utf-8")
            parts.append(ContentPart(type=mime, data=b64_data))
        except Exception as e:
            console.print(f"Error reading image {img.name}: {e}")

    if prompt:
        parts.append(ContentPart(type=MediaType.TEXT, data=prompt))

    return parts


async def process_chat(
    prompt: str,
    images: List[Path],
    files: List[Path],
    config: CompletionConfig,
    memory: bool,
    provider: GeminiProvider,
    vector_search: VectorSearch,
    conversation_id: str,
):
    # 1. Build User Message
    parts = _build_inputs(prompt, images, files)
    if not parts:
        console.print("No input provided.")
        return

    user_msg = Message(role=Role.USER, parts=parts)
    user_text = " ".join([p.data for p in user_msg.parts if p.type == MediaType.TEXT])

    # 2. RAG: Retrieve Memory
    if memory and user_text:
        console.print("Searching memory...")
        results = await vector_search.search(user_text, top_k=3)
        if results:
            context_str = "\n\n".join([f"... {txt} ..." for txt, score in results])
            # Prepend context to user message for the LLM to see
            user_msg.parts.insert(
                0,
                ContentPart(
                    type=MediaType.TEXT, data=f"Relevant past context:\n{context_str}"
                ),
            )
            console.print(f"Found {len(results)} relevant memories.")

            # 3. DB: Save User Message (History)
    db.add_message(conversation_id, user_msg)

    # 4. RAG: Ingest User Message (Memory)
    if user_text:
        await vector_search.ingest(user_text, {"role": "user", "cid": conversation_id})

        # 5. LLM: Generate Response
    history = db.get_conversation_history(conversation_id)
    full_response = ""

    try:
        console.print("Answer: ")

        stream = provider.stream_chat(history, config)

        async for chunk in stream:
            full_response += chunk

        console.print(Markdown(full_response))
        console.print("")

    except Exception as e:
        console.print(f"Generation failed: {e}")
        raise e

        # 6. DB & RAG: Save Model Response
    model_msg = Message(
        role=Role.MODEL, parts=[ContentPart(type=MediaType.TEXT, data=full_response)]
    )
    db.add_message(conversation_id, model_msg)

    if full_response:
        await vector_search.ingest(
            full_response, {"role": "model", "cid": conversation_id}
        )


app = typer.Typer(add_help_option=False, rich_markup_mode=None)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        console.print(
            f"""
    [bold green]
    ██████╗ ██████╗  █████╗  ██████╗  ██████╗ ███╗   ██╗
    ██╔══██╗██╔══██╗██╔══██╗██╔════╝ █     ██╝████╗  ██║
    ██║  ██║██████╔╝███████║██║  ███╗██║   █ ╗██╔██╗ ██║
    ██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║
    ██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝

                 ██████╗ ██╗      █████╗ ███████╗███████╗
                ██╔════╝ ██║     ██╔══██╗██╔════╝██╔════╝
                ██║  ███╗██║     ███████║███████╗███████╗  
                ██║   ██║██║     ██╔══██║╚════██║╚════██║  
                ╚██████╔╝███████╗██║  ██║███████║███████║
                 ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝
    [/bold green]
    $ dg 
    $ cat error.log | dg chat "Analyze the log" 
    $ cat error.log | dg chat "Fix the Error" --image screenshot.png
        """,
            justify="left",
            highlight=True,
        )


@app.command()
def chat(
    prompt: Annotated[str, typer.Argument(help="Input prompt")] = "",
    images: Annotated[Optional[List[Path]], typer.Option("--image", "-i")] = None,
    files: Annotated[Optional[List[Path]], typer.Option("--file", "-f")] = None,
    model: Annotated[
        str, typer.Option("--model", "-m")
    ] = settings.gemini.default_model,
    temperature: Annotated[float, typer.Option("-t")] = settings.gemini.temperature,
    memory: Annotated[bool, typer.Option()] = True,
    conversation_id: Annotated[Optional[str], typer.Option("-c")] = None,
):
    """Start chat or one-off completion."""
    
    # Ensure API key is present before proceeding
    _ensure_api_key()

    async def _run():
        provider = GeminiProvider()
        rag = VectorSearch(provider)
        config = CompletionConfig(model=model, temperature=temperature)

        # Resume or Create Chat
        cid = conversation_id or db.create_conversation(title=prompt[:30] or "New Chat")

        # One-shot or Loop?
        has_input = prompt or _read_stdin() or images or files

        if has_input:
            await process_chat(
                prompt, images or [], files or [], config, memory, provider, rag, cid
            )
        else:
            console.print(f"Interactive Chat (ID: {cid}). Type 'exit' to quit.")
            while True:
                try:
                    p = typer.prompt("You")
                    if p.lower() in ("exit", "quit"):
                        break
                    await process_chat(p, [], [], config, memory, provider, rag, cid)
                except (KeyboardInterrupt, EOFError):
                    break

    asyncio.run(_run())


@app.command()
def log(limit: int = 10):
    """Show recent conversations."""
    rows = [
        [c["id"][:8], c["created_at"], c["title"]]
        for c in db.get_recent_conversations(limit)
    ]
    console.print("History", ["ID", "Date", "Title"], rows)
