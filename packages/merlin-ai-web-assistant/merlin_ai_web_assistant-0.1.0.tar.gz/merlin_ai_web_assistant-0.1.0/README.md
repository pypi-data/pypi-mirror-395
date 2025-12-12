# merlin_ai_helper

A small helper library for AI-powered web assistants using Groq's Llama 3.1 model.

## Installation (local)

In the project root:

```bash
pip install -e merlin_ai_helper

from merlin_ai_helper import get_response, summarize_text, format_response

reply = get_response("Explain cloud computing in simple words.")
print(reply)

summary = summarize_text("Very long text here...")
print(summary)

formatted = format_response(reply, width=60)
print(formatted)


---

### 1.5. `pyproject.toml` – make it an installable package

**File:** `merlin_ai_helper/pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "merlin-ai-helper"  # local package name
version = "0.1.0"
description = "AI helper functions for a Flask web assistant using Groq."
readme = "README.md"
requires-python = ">=3.8"
authors = [
  { name = "Merlin", email = "your-email@example.com" },
]
dependencies = [
  "groq>=0.9.0",
]
