# ScaleXI LLM

A comprehensive multi-provider LLM proxy library that provides a unified interface for interacting with various AI models from different providers.

## 🚀 Features

- **Multi-Provider Support**: OpenAI, Anthropic (Claude), Google (Gemini), Groq, DeepSeek, Alibaba/Qwen, Grok, and Ollama (local OpenAI-compatible)
- **60+ Model Configurations**: Detailed pricing, context lengths, and capabilities for each model
- **Structured Output**: Pydantic schema support with intelligent fallbacks
- **Vision Capabilities**: Image analysis with automatic fallback for non-vision models
- **File Processing**: PDF, DOCX, TXT, and JSON file analysis
- **Web Search Integration**: Multi-provider search via Exa and SERP API (Google)
- **Cost Tracking**: Automatic token usage and cost calculation
- **Robust Fallbacks**: Multi-level fallback mechanisms for reliability
- **Comprehensive Testing**: Built-in benchmarking across all providers

### Latest Model Support (Dec 2025)

The current release ships configuration for the newest flagship models across top providers:

- **Anthropic**: Claude 4.5 family (`claude-haiku-4-5`, `claude-sonnet-4-5`, `claude-opus-4-5` + thinking variants)
- **Google**: `gemini-3-pro-preview` alongside refreshed Gemini 2.5 tiers
- **Grok (xAI)**: `grok-4-fast-*` and `grok-4-1-fast-*` reasoning / non-reasoning variants with 2M context

See `documentation.html` → *Model Reference* for full capability/pricing tables.

## 📦 Installation

```bash
# Clone the repository
git clone <repository-url>
cd scalexi_llm

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

```
openai
anthropic
google-genai
groq
pymupdf
xai-sdk
python-docx
pydantic
python-dotenv
exa-py
serpapi
```

## ⚙️ Configuration

Set up your API keys using either method:

### Option 1: `.env` File (Recommended for Local Development)

Create a `.env` file in the project root:

```env
# Provider API Keys (only set the ones you need)
OPENAI_API_KEY=your_openai_key          # For GPT models
ANTHROPIC_API_KEY=your_anthropic_key    # For Claude models
GEMINI_API_KEY=your_gemini_key          # For Gemini models
GROQ_API_KEY=your_groq_key              # For Groq models
DEEPSEEK_API_KEY=your_deepseek_key      # For DeepSeek models
QWEN_API_KEY=your_qwen_key              # For Qwen models (alibaba cloud)
GROK_API_KEY=your_grok_key              # For Grok (xAI) models

# Search API Keys (optional, for web search features)
EXA_API_KEY=your_exa_key                # For Exa search
SERP_API_KEY=your_serp_key              # For Google search via SERP API
```

### Option 2: Direct Export (Good for CI/Containers)

```bash
export OPENAI_API_KEY=your_openai_key
export ANTHROPIC_API_KEY=your_anthropic_key
export GEMINI_API_KEY=your_gemini_key
# ... add only the keys you need
```

**Note**: `LLMProxy` reads keys via `os.getenv()`, so any method that sets environment variables works. Only include API keys for providers you intend to use—missing keys simply disable that provider. Some providers may fallback to Gemini in certain cases (see documentation for details).

## 🔧 Quick Start

```python
from scalexi_llm import LLMProxy

# Initialize the proxy
llm = LLMProxy()

# Basic usage
response, execution_time, token_usage, cost = llm.ask_llm(
    model_name="gemini-2.5-flash",
    system_prompt="You are a helpful assistant.",
    user_prompt="Explain quantum computing in simple terms"
)

print(f"Response: {response}")
print(f"Cost: ${cost:.6f}")
print(f"Tokens used: {token_usage['total_tokens']}")
```

### Verbosity Control

Control console logging from `LLMProxy` and its internal logger using the optional `verbose` parameter during initialization.

**Verbosity Levels:**
- `0` — Silent (only critical errors)
- `1` — Normal (default - shows helpful info, warnings, and stats/metadata)
- `2` — Debug (includes search results, and llm call results)

**Default**: `verbose=1` (normal logging)

```python
# Silent mode (minimal output)
llm = LLMProxy(verbose=0)

# Normal mode (default - no need to specify)
llm = LLMProxy()  # or LLMProxy(verbose=1)

# Debug mode (detailed logging)
llm = LLMProxy(verbose=2)
```

## 💡 Usage Examples

### Structured Output

```python
from pydantic import BaseModel, Field
from typing import List

class Recipe(BaseModel):
    name: str = Field(description="Recipe name")
    ingredients: List[str] = Field(description="Required ingredients")
    steps: List[str] = Field(description="Cooking steps")
    cooking_time: int = Field(description="Cooking time in minutes")

response, _, _, _ = llm.ask_llm(
    model_name="gpt-4o-latest",
    user_prompt="Create a recipe for chocolate chip cookies",
    schema=Recipe
)
```

### Image Analysis

```python
response, _, _, _ = llm.ask_llm(
    model_name="moonshotai/kimi-k2-instruct",
    user_prompt="Analyze this image and describe what you see",
    image_path="photo.jpg"
)
```

### File Processing

```python
response, _, _, _ = llm.ask_llm(
    model_name="claude-sonnet-4-0",
    user_prompt="Summarize this document",
    file_path="document.pdf"
)
```

### Web Search with Different Providers

```python
# Using Exa (default)
response, _, _, _ = llm.ask_llm(
    model_name="claude-3-7-sonnet-latest",
    user_prompt="Latest AI developments in 2024",
    websearch=True
)

# Using SERP API (Google)
response, _, _, _ = llm.ask_llm(
    model_name="chatgpt-4o-latest",
    user_prompt="Current trends in quantum computing",
    websearch=True,
    search_tool="serp",
    max_search_results=10
)

# Using both Exa + SERP for maximum coverage
response, _, _, _ = llm.ask_llm(
    model_name="gemini-2.5-pro",
    user_prompt="Comprehensive market analysis",
    websearch=True,
    search_tool="both",
    max_search_results=15
)

# With query generator (AI optimizes the search query)
response, _, _, _ = llm.ask_llm(
    model_name="claude-sonnet-4-0",
    user_prompt="Python machine learning tutorials",
    websearch=True,
    use_query_generator=True  # Enable AI query optimization
)
```

### Combined Features

```python
response, _, _, _ = llm.ask_llm(
    model_name="grok-4-latest",
    system_prompt="Analyze the provided content comprehensively",
    user_prompt="Analyze this resume and find career recommendations from web.",
    file_path="resume.pdf",
    image_path="certifications.png",
    websearch=True,
    schema=AnalysisSchema
)
```

## 🔄 Fallback Mechanisms

The library implements intelligent fallback systems:

1. **Vision Fallback**: Non-vision models automatically use vision-capable models from the same provider to describe images
2. **Structured Output Fallback**: Falls back to better models from the same provider when schema validation fails

Models from certain providers fallback to Gemini in certain cases.
Check documentation for more details on fallbacks.

## 🧪 Testing

### Multi-Provider Feature Tests (Recommended)

Test all 8 providers with 4 test scenarios each (unstructured, structured file/image/web):

```bash
cd testing
python provider_test.py
```

### Focused Ollama Test

Test local Ollama models specifically:

```bash
cd testing
python ollama_test.py
```

### Full Benchmark Suite (Optional)

Run comprehensive benchmarking across all available models:

```bash
cd testing
python combined_test.py
```

This will:
- Test 60+ models across all providers
- Benchmark performance and cost
- Generate detailed analysis reports
- Test combined features (file + image + web search + structured output)

**Note**: Full benchmark can take several hours. Use `provider_test.py` for quick regression testing.

## 📊 Cost Tracking

Every request returns detailed cost and token usage information:

```python
response, execution_time, token_usage, cost = llm.ask_llm(...)

# Token usage breakdown
print(token_usage)
# {
#     "prompt_tokens": 150,
#     "completion_tokens": 200,
#     "total_tokens": 350
# }

# Total cost in USD
print(f"Cost: ${cost:.6f}")
```

## 🛠️ API Reference

### `ask_llm()` Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model_name` | str | `"gpt-4o-mini"` | Model to use for generation |
| `system_prompt` | str | `""` | System prompt for the model |
| `user_prompt` | str | `""` | User prompt/message |
| `temperature` | float | `None` | Sampling temperature (0.0-2.0) |
| `schema` | Pydantic Model | `None` | Structured output schema |
| `image_path` | str | `None` | Path to image file |
| `file_path` | str | `None` | Path to file for analysis |
| `websearch` | bool | `False` | Enable web search |
| `use_query_generator` | bool | `False` | Use AI to generate optimized search query |
| `max_search_results` | int | `12` | Maximum search results to retrieve |
| `search_tool` | str | `"exa"` | Search provider: "exa", "serp", or "both" |
| `max_tokens` | int | `None` | Maximum tokens to generate |
| `retry_limit` | int | `1` | Number of retry attempts |
| `fallback_to_provider_best_model` | bool | `True` | Enable provider fallback |
| `fallback_to_standard_model` | bool | `True` | Enable cross-provider fallback |

### Return Values

Returns a tuple: `(response, execution_time, token_usage, cost)`

- **response**: The model's response (string or JSON)
- **execution_time**: Time taken in seconds (float)
- **token_usage**: Dictionary with token counts
- **cost**: Total cost in USD (float)

---

**ScaleXI LLM** - Unified AI model access with enterprise-grade reliability and comprehensive feature support.