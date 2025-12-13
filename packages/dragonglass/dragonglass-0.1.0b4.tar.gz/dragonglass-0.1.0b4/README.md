# DragonGlass

<div>

![DragonGlass CLI](https://img.shields.io/badge/Status-Beta-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-FFE873?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-Powered-4285F4?style=for-the-badge&logo=google&logoColor=white)

**LLM CLI engineered for developer workflows.** 
Built on **Hexagonal Architecture** for strict typing, modularity, and speed.

</div>

---
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
   
    $ dg 
    $ cat error.log | dg chat "Analyze the log" 
    $ cat error.log | dg chat "Fix the Error" --image screenshot.png
## Features

 
Optimized for the Google Gemini ecosystem.
- **Multimodal**: Native support for text, images, and audio.
- **Fast**: Streams responses in real-time.
- **Efficient**: Uses `gemini-embedding-001` for high-quality semantic search.
- **Unix Philosophy**: Designed to be piped.
  - cat logs.txt | dg chat "Analyze this error" --image screenshot.png
- **Hexagonal Architecture**: Core logic is completely decoupled from infrastructure (DB, API).
- **XDG Compliant**: respect your system's config standards (`~/.config/dg`, `~/.local/share/dg`).

## Installation

Requires **Python 3.10+**.

```bash
pipx install dragonglass
```

## Configuration

Set your Gemini API key via environment variable:

```

Linux: ~/.config/dg/config.toml                                           
macOS: ~/Library/Application Support/dg/config.toml

# config.toml
    [gemini]
    google_api_key="A....D2E"
    default_model="gemini-3-pro-preview"
    temperature=0.7
    top_p=1.0
    safe_settings="BLOCK_NONE"
    grounding_enabled=true


```

Or run a command, and `dg` will guide you.

## Usage

```bash
cat error.log | python -m dg chat "Fix this error" --image screenshot.png # Multimodal One-Shot (Pipe + Image)
```

### Pipelines
Process files and data streams.

```bash
# Summarize a README
cat README.md | dg chat "Summarize the key features"
```

### History
View your conversation logs.

```bash
dg log
```

## Roadmap

- [x] Core Architecture (Hexagonal)
- [x] Gemini Integration (Streaming)
- [x] SQLite Persistence
- [x] Local RAG (Numpy + Embeddings)
- [ ] **Interactive TUI**: Full chat interface with `Textual`.
- [x] **Multimodal Inputs**: `dg chat --image screenshot.png "Fix this UI"`
- [ ] **Project Awareness**: Auto-index git repositories for context.



## LICENSE

Apache License 2.0