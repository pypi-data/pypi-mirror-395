# ScaleXI LLM

A production-ready, multi-provider LLM proxy that gives you **one unified API** for many different model providers.

- **8 Providers**: OpenAI, Anthropic (Claude), Google (Gemini), Groq, DeepSeek, Alibaba/Qwen, Grok, and local **Ollama** (OpenAI-compatible)
- **60+ Model Configurations**: Pricing, limits, and capabilities encoded in a single model registry
- **Structured Outputs**: Pydantic schemas with intelligent fallbacks and validation
- **Vision & Files**: Image analysis, PDF/DOCX/TXT/JSON handling, and automatic vision fallbacks
- **Web Search**: Exa + SERP (Google) integration for retrieval-augmented generation
- **Fallbacks & Reliability**: Provider-best and global-standard fallbacks, plus detailed error logging

This package is ideal when you want a **single, consistent interface** to multiple LLM vendors, with:

- Centralized configuration for models and costs
- Unified ask function (`ask_llm`) that works across providers
- Built-in support for web search, files, and images
- Optional local-only workflows via Ollama

## Installation

```bash
pip install scalexi_llm
```

## Quick Example

```python
from scalexi_llm import LLMProxy

llm = LLMProxy()

response, execution_time, token_usage, cost = llm.ask_llm(
    model_name="chatgpt-4o-latest",
    system_prompt="You are a helpful assistant.",
    user_prompt="Explain quantum computing in simple terms."
)

print(response)
```

## Features at a Glance

- One `LLMProxy` class for all providers
- Unified `ask_llm` API for text, files, images, and web search
- Pydantic-based structured outputs with retry and model fallbacks
- Vision fallback when a chosen model doesn’t support images
- Token and cost accounting for every call
- Comprehensive test suite (`provider_test.py`, `ollama_test.py`, `combined_test.py`)

## Documentation & Source

- **Full docs & examples**: see the GitHub repository README and `documentation.html` in the repo
- **Source code**: https://github.com/scalexi/scalexi_llm

Use `scalexi_llm` when you want a **single, robust integration layer** instead of juggling multiple vendor SDKs and APIs.
