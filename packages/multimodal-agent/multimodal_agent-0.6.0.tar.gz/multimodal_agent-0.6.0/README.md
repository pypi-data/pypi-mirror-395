# **Multimodal-Agent**

*A lightweight, production-ready multimodal wrapper for Google Gemini with RAG, image input, JSON mode, project learning, session memory, and a clean CLI & server.*

---

## Features

### Core LLM Capabilities

- **Text generation**
- **Image + text multimodal input**
- **Response formatting (syntax-aware, v0.4.0+)**
- **JSON mode with stable pretty-printing**
- **Automatic language detection**

### RAG + Memory

- **SQLite vector store**
- **Persistent conversation memory**
- **Chunking + embedding storage**
- **Cosine similarity search**
- **Session-aware chat**
- **`~/.multimodal_agent/memory.db`**

### Server (FastAPI, v0.5.0+)

* `/ask`
* `/ask_with_image`
* `/generate`
* `/memory/search`
* `/learn/project`
* `/project_profiles/list`

Includes:

* Safe error handling
* Offline fake-response mode
* Test coverage for all endpoints

### Development Tools (v0.6.0)

* **Flutter / code project analysis**
* **Project-style learning (auto-extract architecture, state management, linting, etc.)**
* **Extensible foundation for VS Code & Flutter extension generators**

---

## Installation

```bash
pip install multimodal-agent
```

Or local:

```bash
pip install -e .
```

Set your Google API key:

```bash
export GOOGLE_API_KEY="your-key"
```

**No API key?**

The agent automatically falls back to **FakeResponse offline mode** for testing & debugging.

---

## Quick Start
### **Text Question**

```bash
agent ask "hello"
```

### **Disable RAG**

```bash
agent ask "hello" --no-rag
```

### **JSON mode**

```bash
agent ask "give me json" --json
```

### **Image + Text**

```bash
agent image test.jpg "describe this"
```

### **Chat (with persistent memory)**

```bash
agent chat
```

---

### RAG (Built-in)

Your memory DB lives at:

```bash
~/.multimodal_agent/memory.db
```
**To clear memory:**
```bash
agent clear
```

RAG includes:

* chunking
* embeddings
* cosine similarity
* session grouping
* project-learning style profiles (v0.6.0)

---

### Project Learning (v0.6.0)

The agent can scan a project and learn its structure.

Example:

```bash
curl -X POST http://127.0.0.1:8000/learn/project \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/flutter/project"}'
```

This extracts:

* package name
* architecture patterns
* linting rules
* state management
* file counts
* widget usage patterns
* build_runner / freezed usage
* and stores a **profile** in SQLite

List learned profiles:

```bash
curl http://127.0.0.1:8000/project_profiles/list
```

---

### Server Mode

Start:

```bash
agent server
```

Runs at:

```
http://127.0.0.1:8000
```
## API Reference (v0.6.0)
## **POST /ask**

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "hello"}'
```

Response:

```json
{
  "text": "hello",
  "data": null,
  "usage": { "prompt_tokens": 44, "response_tokens": 3, "total_tokens": 553 }
}
```
## **POST /ask_with_image**
```bash
curl -X POST http://127.0.0.1:8000/ask_with_image \
  -F "file=@test.jpg" \
  -F "prompt=describe this"
```
### v0.6.0 Better Error Handling

Failures now return:

```json
{
  "text": "Image processing failed: 429 RESOURCE_EXHAUSTED ...",
  "data": null,
  "usage": {},
  "error": true
}
```

Never returns `text: null`.

---

## **POST /generate**

```bash
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "give me json", "json": true}'
```

---

## **POST /memory/search**

```bash
curl -X POST http://127.0.0.1:8000/memory/search \
  -H "Content-Type: application/json" \
  -d '{"query": "hello"}'
```

Response:

```json
{
  "results": [
    [0.98, { "id": 1, "content": "hello", "role": "user" }]
  ]
}
```

---

## **POST /learn/project**

Returns a structured project profile:

```json
{
  "status": "ok",
  "project_id": "project:rope_simulation_using_flutter",
  "profile": {
    "package_name": "rope_simulation_using_flutter",
    "architecture": {
      "patterns": ["feature_first"],
      "state_management": []
    },
    "dart_files_count": 3,
    "widget_files_count": 2
  }
}
```

---

## Architecture Overview
```bash
multimodal_agent/
    core/          # Main agent logic
    rag/           # SQLite vector store
    cli/           # CLI commands (`agent`)
    server/        # FastAPI server implementation
    utils/         # helpers
```

### Memory schema:

```bash
sessions      # chat sessions
chunks        # tokenized fragments
embeddings    # vector embeddings
projects      # project profiles (v0.6.0)
```

---

## **Formatting Engine (v0.4.0+)**

* Detects JSON, XML, HTML, code, python, kotlin, dart, js, swift …
* Pretty-prints output
* Auto-wraps in fenced code blocks
* Optional in `agent.ask(formatted=True)`

---

## Running Tests

```bash
make test
make coverage
```

160+ tests cover:

* server
* embeddings
* chat memory
* RAG
* CLI commands
* project learning
* JSON mode
* offline fake mode

---

## Roadmap

### **v0.6.x**

* VS Code & JetBrains extension
* Flutter extension (code generator + project insights)

### **v0.7.x**

* Streaming responses
* Pluggable embedding backends (Gemini / local / offline)

### **v1.0**

* Stable API
* Plugin ecosystem
* Multi-language project analyzers

---

# License

MIT License.
