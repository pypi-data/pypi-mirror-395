# **Multimodal-Agent**

*A lightweight, production-ready multimodal wrapper for Google Gemini with optional RAG, image input, JSON mode, and a clean CLI.*

---

## Features

- **Text generation**
- **Image + text multimodal input**
- **RAG memory store (SQLite)**
- **Server mode (FastAPI)**
- **Clean CLI (`agent`)**
- **Retry logic + error handling**
- **JSON mode**
- **Token usage logging**
- **Syntax-aware output formatting**
- **Session-aware chat with persistent memory**
- Added **Server API**, **full RAG flow**, **image upload**, **memory search**, and more.


## Installation

```bash
pip install multimodal-agent
```
Or local:

```bash
pip install -e .
```
Requires:

- Python 3.10+

- A Google API key `(GOOGLE_API_KEY)`

```bash
export GOOGLE_API_KEY="your-key-here"
```

Without a key, the package still works using offline FakeResponse for testing & debugging.

## Quick Start
**Text Question**
```bash
agent ask "hello"
```
Output:

```shell
## Question
hello

## Answer
hello
```
**Disable RAG:**
```bash
agent ask "hello" --no-rag
```
**JSON mode**
```bash
agent ask "give me json" --json
```
## Image + Text Input
```bash
agent image test.jpg "describe this"
```
## Chat Mode (Persistent Memory)
```bash
agent chat
```

Features:

- Session aware

- Stores conversation chunks

- Embeds each message

- Retrieves similar chunks (RAG)

- Generates response

- Logs usage

Exit with:

```bash
exit
```
## RAG (Retrieval-Augmented Generation)
RAG is fully built in:
- SQLite storage
- Chunked messages
- Embedding storage
- Cosine-based similarity search
- Used automatically during `ask()` and `chat()`

Your DB lives at:

```bash
~/.multimodal_agent/memory.db
```
**To clear memory:**
```bash
agent clear
```
---
### Run as a Server (FastAPI)
Start server:

```bash
agent server
```
Runs at:

```bash
http://127.0.0.1:8000
```
## API Reference (v0.5.0)
### POST /ask
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "hello"}'
```
Request:

```json
{
  "prompt": "hello",
  "response_format": null,
  "session_id": null,
  "no_rag": false
}
```
Response:

```json
{
  "text": "hello",
  "data": null,
  "usage": { "prompt_tokens": 44, "response_tokens": 1, "total_tokens": 553 }
}
```
### POST /ask_with_image
```bash
curl -X POST http://127.0.0.1:8000/ask_with_image \
  -F "file=@test.jpg" \
  -F "prompt=describe this"
```
### POST /generate
```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "give me json", "json": true}'
```
### POST /memory/search
```bash
curl -X POST http://127.0.0.1:8000/memory/search \
  -H "Content-Type: application/json" \
  -d '{"query": "hello", "limit": 5}'
Returns ranked similar memory chunks:

```json
{
  "results": [
    [1.0, { "id": 331, "content": "hello", "role": "agent" }]
  ]
}
```
## Architecture Overview
```bash
multimodal_agent/
    core/          # Agent logic
    rag/           # SQLite store + embeddings
    cli/           # Command-line interface
    server/        # FastAPI server
    utils/         # helper functions
```
Memory DB:
```bash
sessions  — chat sessions
chunks    — tokenized text fragments
embeddings — vector store
```
**JSON + Image Mode Support**
Usage logging works seamlessly across:
- ask()
- ask_with_image()
- response_format="json"
- offline FakeResponse mode

Logging is  **silent** , non-blocking, and wrapped in safe try/except guards.

It never interferes with the agent and never breaks tests.

## **Formatting Engine (v0.4.0)**

Multimodal-Agent now includes a robust formatter that automatically detects and beautifies output.

Supported types:

* **JSON** → pretty-printed, stable formatting
* **Code** → wrapped in triple backticks with detected language
* **XML / HTML** → pretty printed
* **Plain text** → normalized

### Usage:

<pre class="overflow-visible!" data-start="1133" data-end="1217"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>resp = agent.ask(</span><span>"write python code"</span><span>, formatted=</span><span>True</span><span>)
</span><span>print</span><span>(resp.text)
</span></span></code></div></div></pre>

Example output:

<pre class="overflow-visible!" data-start="1236" data-end="1299"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-markdown"><span><span>
def add(a, b):
    return a + b
</span></span></code></div></div></pre>
## **Language Detection (v0.4.0)**

The formatter uses the internal `detect_language()` to identify code automatically.

Detected languages include:

* Python
* JavaScript
* Java
* Kotlin
* Swift
* Objective-C
* Dart
* C++
* JSON
* XML/HTML
* Plain text

### Example:

<pre class="overflow-visible!" data-start="1696" data-end="1828"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> multimodal_agent.formatting </span><span>import</span><span> detect_language

</span><span>print</span><span>(detect_language(</span><span>"fun greet(name: String)"</span><span>))  </span><span># → kotlin</span></span></code></div></div></pre>

## **Agent server mode (v0.5.0)**

- Full FastAPI server 

- `/ask`, `/ask_with_image`, `/memory/search`, `/generate`

- Production-ready RAG

- CLI + server parity

- Stable chunking

- SQLite-backed memory

- Fully tested (130+ passing tests)

## Running Testing
```bash
make test
make coverage
```
All tests reside in:

```bash
src/multimodal_agent/tests
```
130+ tests, including server, RAG, embedding, core agent, and CLI.

## Roadmap
v0.5.x - Improve server streaming and Authentication

v0.6.0 - VS Code extension




# License

MIT License.
