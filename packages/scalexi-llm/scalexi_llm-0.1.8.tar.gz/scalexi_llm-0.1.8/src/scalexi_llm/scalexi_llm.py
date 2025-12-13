from __future__ import annotations
import os
import json
import base64
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
from docx import Document
from typing import Optional
from pydantic import BaseModel
#from pydantic_processor import PydanticGuidelinesProcessor # experimental, might be removed
from openai import OpenAI
from xai_sdk import Client as grok_client
from xai_sdk.chat import system, user, image
from google.genai import Client as google_client
from google.genai import types
from groq import Groq
import anthropic
from exa_py import Exa
import pymupdf
import httpx
import requests
from serpapi import GoogleSearch
import time
import traceback
import warnings
warnings.filterwarnings("ignore")
import pprint

# Define model-specific configurations
MODEL_CONFIGS = {
    "gpt-4o-mini": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 0.15 * 1e-6,
        "price_per_completion_tokens": 0.6 * 1e-6,
        "context_length": 128000,
        "max_tokens": 16000,
        "client_config": {
            "api_key_env": "OPENAI_API_KEY",
            "base_url": "https://api.openai.com/v1",
            "client_class": "OpenAI"
        }
    },
    "gpt-5": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 1.25 * 1e-6,                 
        "price_per_completion_tokens": 10.00 * 1e-6,         
        "context_length": 256000,                            
        "max_tokens": 128000,
        "reasoning_effort": "medium",                  
        "client_config": {
            "api_key_env": "OPENAI_API_KEY",
            "base_url": "https://api.openai.com/v1",
            "client_class": "OpenAI"
        }
    },
    "gpt-4o": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 2.50 * 1e-6,
        "price_per_completion_tokens": 10.00 * 1e-6,
        "context_length": 128000,
        "max_tokens": 16000,
        "client_config": {
            "api_key_env": "OPENAI_API_KEY",
            "base_url": "https://api.openai.com/v1",
            "client_class": "OpenAI"
        }
    },
    "gpt-4.1": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 2.00 * 1e-6,
        "price_per_completion_tokens": 8.00 * 1e-6,
        "context_length": 1000000,
        "max_tokens": 32000,
        "client_config": {
            "api_key_env": "OPENAI_API_KEY",
            "base_url": "https://api.openai.com/v1",
            "client_class": "OpenAI"
        }
    },
    "gpt-4.1-mini": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 0.40 * 1e-6,
        "price_per_completion_tokens": 1.60 * 1e-6,
        "context_length": 1000000,
        "max_tokens": 32000,
        "client_config": {
            "api_key_env": "OPENAI_API_KEY",
            "base_url": "https://api.openai.com/v1",
            "client_class": "OpenAI"
        }
    },
    "gpt-4.1-nano": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 0.1 * 1e-6,
        "price_per_completion_tokens": 0.4 * 1e-6,
        "context_length": 1000000,
        "max_tokens": 32000,
        "client_config": {
            "api_key_env": "OPENAI_API_KEY",
            "base_url": "https://api.openai.com/v1",
            "client_class": "OpenAI"
        }
    },
    "chatgpt-4o-latest": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 5.0 * 1e-6,
        "price_per_completion_tokens": 15.00 * 1e-6,
        "context_length": 128000,
        "max_tokens": 16000,
        "client_config": {
            "api_key_env": "OPENAI_API_KEY",
            "base_url": "https://api.openai.com/v1",
            "client_class": "OpenAI"
        }
    },
    "o1": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 15.0 * 1e-6,
        "price_per_completion_tokens": 60.00 * 1e-6,
        "context_length": 200000,
        "max_tokens": 100000,
        "reasoning_effort": "high",
        "client_config": {
            "api_key_env": "OPENAI_API_KEY",
            "base_url": "https://api.openai.com/v1",
            "client_class": "OpenAI"
        }
    },
    "o3": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 2.00 * 1e-6,
        "price_per_completion_tokens": 8.00 * 1e-6,
        "context_length": 200000,
        "max_tokens": 100000,
        "reasoning_effort": "high",
        "client_config": {
            "api_key_env": "OPENAI_API_KEY",
            "base_url": "https://api.openai.com/v1",
            "client_class": "OpenAI"
        }
    },
    "o3-mini": {
        "structured_output": True,
        "vision": False,
        "price_per_prompt_tokens": 1.1 * 1e-6,
        "price_per_completion_tokens": 4.40 * 1e-6,
        "context_length": 200000,
        "max_tokens": 100000,
        "reasoning_effort": "medium",
        "client_config": {
            "api_key_env": "OPENAI_API_KEY",
            "base_url": "https://api.openai.com/v1",
            "client_class": "OpenAI"
        }
    },
    "o4-mini": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 1.1 * 1e-6,
        "price_per_completion_tokens": 4.40 * 1e-6,
        "context_length": 200000,
        "max_tokens": 100000,
        "reasoning_effort": "high",
        "client_config": {
            "api_key_env": "OPENAI_API_KEY",
            "base_url": "https://api.openai.com/v1",
            "client_class": "OpenAI"
        }
    },
    "deepseek-chat": {
        "structured_output": True,
        "vision": False,
        "price_per_prompt_tokens": 0.56 * 1e-6,
        "price_per_completion_tokens": 1.68 * 1e-6,
        "context_length": 64000,
        "max_tokens": 8096,
        "client_config": {
            "api_key_env": "DEEPSEEK_API_KEY",
            "base_url": "https://api.deepseek.com",
            "client_class": "DeepSeek"
        },
        "prompt_limit": 70000
    },
    "deepseek-reasoner": {
        "structured_output": True,
        "vision": False,
        "price_per_prompt_tokens": 0.56 * 1e-6,
        "price_per_completion_tokens": 1.68 * 1e-6,
        "context_length": 64000,
        "max_tokens": 8096,
        "client_config": {
            "api_key_env": "DEEPSEEK_API_KEY",
            "base_url": "https://api.deepseek.com",
            "client_class": "DeepSeek"
        },
        "prompt_limit": 70000
    },
    "llama-3.1-8b-instant": {
        "structured_output": False,
        "vision": False,
        "price_per_prompt_tokens": 0.05 * 1e-6,
        "price_per_completion_tokens": 0.08 * 1e-6,
        "context_length": 131000,
        "max_tokens": 131000,
        "client_config": {
            "api_key_env": "GROQ_API_KEY",
            "client_class": "Groq"
        },
        "free_tier": {
            "max_tokens": 7999,
            "prompt_limit": 6000
        }
    },
    "llama-3.3-70b-versatile": {
        "structured_output": False,
        "vision": False,
        "price_per_prompt_tokens": 0.59 * 1e-6,
        "price_per_completion_tokens": 0.79 * 1e-6,
        "context_length": 131000,
        "max_tokens": 32000,
        "client_config": {
            "api_key_env": "GROQ_API_KEY",
            "client_class": "Groq"
        },
        "free_tier": {
            "max_tokens": 7999,
            "prompt_limit": 6000
        }
    },
    "deepseek-r1-distill-llama-70b": {
        "structured_output": False,
        "vision": False,
        "price_per_prompt_tokens": 0.75 * 1e-6,
        "price_per_completion_tokens": 0.99 * 1e-6,
        "context_length": 16000,
        "max_tokens": 16000,
        "client_config": {
            "api_key_env": "GROQ_API_KEY",
            "client_class": "Groq"
        },
        "free_tier": {
            "max_tokens": 7999,
            "prompt_limit": 6000
        }
    },
    "moonshotai/kimi-k2-instruct": {
        "structured_output": True,
        "vision": False,
        "price_per_prompt_tokens": 1.00 * 1e-6,
        "price_per_completion_tokens": 3.00 * 1e-6,
        "context_length": 131072,
        "max_tokens": 16384,
        "client_config": {
            "api_key_env": "GROQ_API_KEY",
            "client_class": "Groq"
        },
        "free_tier": {
            "max_tokens": 7999,
            "prompt_limit": 6000
        }
    },
    "openai/gpt-oss-120b": {
        "structured_output": True,
        "vision": False,
        "price_per_prompt_tokens": 0.15 * 1e-6,
        "price_per_completion_tokens": 0.75 * 1e-6,
        "context_length": 131072,
        "max_tokens": 65526,
        "client_config": {
            "api_key_env": "GROQ_API_KEY",
            "client_class": "Groq"
        },
        "free_tier": {
            "max_tokens": 7999,
            "prompt_limit": 6000
        }
    },
    "openai/gpt-oss-20b": {
        "structured_output": True,
        "vision": False,
        "price_per_prompt_tokens": 0.10 * 1e-6,
        "price_per_completion_tokens": 0.50 * 1e-6,
        "context_length": 131072,
        "max_tokens": 65526,
        "client_config": {
            "api_key_env": "GROQ_API_KEY",
            "client_class": "Groq"
        },
        "free_tier": {
            "max_tokens": 7999,
            "prompt_limit": 6000
        }
    },
    "meta-llama/llama-4-scout-17b-16e-instruct": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 0.11 * 1e-6,
        "price_per_completion_tokens": 0.34 * 1e-6,
        "context_length": 	131072,
        "max_tokens": 8192,
        "client_config": {
            "api_key_env": "GROQ_API_KEY",
            "client_class": "Groq"
        },
        "free_tier": {
            "max_tokens": 7999,
            "prompt_limit": 6000
        }
    },
    "meta-llama/llama-4-maverick-17b-128e-instruct": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 0.20 * 1e-6,
        "price_per_completion_tokens": 0.60 * 1e-6,
        "context_length": 	131072,
        "max_tokens": 8192,
        "client_config": {
            "api_key_env": "GROQ_API_KEY",
            "client_class": "Groq"
        },
        "free_tier": {
            "max_tokens": 7999,
            "prompt_limit": 6000
        }
    },
    "qwen-max-latest": {
        "structured_output": False,
        "vision": False,
        "price_per_prompt_tokens": 1.6 * 1e-6,
        "price_per_completion_tokens": 6.4 * 1e-6,
        "context_length": 30720,
        "max_tokens": 8192,
        "client_config": {
            "api_key_env": "QWEN_API_KEY",
            "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            "client_class": "Alibaba"
        }
    },
    "qwen-turbo-latest": {
        "structured_output": False,
        "vision": False,
        "price_per_prompt_tokens": 0.05 * 1e-6,
        "price_per_completion_tokens": 0.2 * 1e-6,
        "context_length": 1000000,
        "max_tokens": 16384,
        "client_config": {
            "api_key_env": "QWEN_API_KEY",
            "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            "client_class": "Alibaba"
        }
    },
    "qwen-plus-latest": {
        "structured_output": False,
        "vision": False,
        "price_per_prompt_tokens": 0.4 * 1e-6,
        "price_per_completion_tokens": 1.2 * 1e-6,
        "context_length": 995904,
        "max_tokens": 32768,
        "client_config": {
            "api_key_env": "QWEN_API_KEY",
            "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            "client_class": "Alibaba"
        }
    },
    "qwen-flash": {
        "structured_output": False,
        "vision": False,
        "price_per_prompt_tokens": 0.05 * 1e-6,
        "price_per_completion_tokens": 0.40 * 1e-6,
        "context_length": 1000000,
        "max_tokens": 32768,
        "client_config": {
            "api_key_env": "QWEN_API_KEY",
            "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            "client_class": "Alibaba"
        }
    },
    "qwen3-235b-a22b-thinking-2507": {
        "structured_output": False,
        "vision": False,
        "price_per_prompt_tokens": 0.7 * 1e-6,
        "price_per_completion_tokens": 8.4 * 1e-6,
        "context_length": 126976,
        "max_tokens": 32768,
        "client_config": {
            "api_key_env": "QWEN_API_KEY",
            "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            "client_class": "Alibaba"
        }
    },
    "qwen3-235b-a22b-instruct-2507": {
        "structured_output": False,
        "vision": False,
        "price_per_prompt_tokens": 0.7 * 1e-6,
        "price_per_completion_tokens": 2.8 * 1e-6,
        "context_length": 129024,
        "max_tokens": 32768,
        "client_config": {
            "api_key_env": "QWEN_API_KEY",
            "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            "client_class": "Alibaba"
        }
    },
    "qwen3-30b-a3b-thinking-2507": {
        "structured_output": False,
        "vision": False,
        "price_per_prompt_tokens": 0.2 * 1e-6,
        "price_per_completion_tokens": 2.4 * 1e-6,
        "context_length": 126976,
        "max_tokens": 32768,
        "client_config": {
            "api_key_env": "QWEN_API_KEY",
            "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            "client_class": "Alibaba"
        }
    },
    "qwen3-30b-a3b-instruct-2507": {
        "structured_output": False,
        "vision": False,
        "price_per_prompt_tokens": 0.20 * 1e-6,
        "price_per_completion_tokens": 0.80 * 1e-6,
        "context_length": 126976,
        "max_tokens": 32768,
        "client_config": {
            "api_key_env": "QWEN_API_KEY",
            "base_url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            "client_class": "Alibaba"
        }
    },
    "grok-3-mini-latest": {
        "structured_output": True,
        "vision": False,
        "price_per_prompt_tokens": 0.30 * 1e-6,
        "price_per_completion_tokens": 0.50 * 1e-6,
        "context_length": 131072,
        "max_tokens": 131072,
        "client_config": {
            "api_key_env": "GROK_API_KEY",
            "base_url": "https://api.x.ai/v1",
            "client_class": "Grok"
        }
    },
    "grok-3-latest": {
        "structured_output": True,
        "vision": False,
        "price_per_prompt_tokens": 3.00 * 1e-6,
        "price_per_completion_tokens": 15.00 * 1e-6,
        "context_length": 131072,
        "max_tokens": 131072,
        "client_config": {
            "api_key_env": "GROK_API_KEY",
            "base_url": "https://api.x.ai/v1",
            "client_class": "Grok"
        }
    },
    "grok-3-mini-fast-latest": {
        "structured_output": True,
        "vision": False,
        "price_per_prompt_tokens": 0.60 * 1e-6,
        "price_per_completion_tokens": 4.00 * 1e-6,
        "context_length": 131072,
        "max_tokens": 131072,
        "client_config": {
            "api_key_env": "GROK_API_KEY",
            "base_url": "https://api.x.ai/v1",
            "client_class": "Grok"
        }
    },
    "grok-4-latest": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 3.00 * 1e-6,
        "price_per_completion_tokens": 15.00 * 1e-6,
        "context_length": 256000,
        "max_tokens": 256000,
        "client_config": {
            "api_key_env": "GROK_API_KEY",
            "base_url": "https://api.x.ai/v1",
            "client_class": "Grok"
        }
    },
    "grok-4-fast-non-reasoning": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 0.20 * 1e-6,
        "price_per_completion_tokens": 0.50 * 1e-6,
        "context_length": 2000000,
        "max_tokens": 256000,
        "client_config": {
            "api_key_env": "GROK_API_KEY",
            "base_url": "https://api.x.ai/v1",
            "client_class": "Grok"
        }
    },
    "grok-4-fast-reasoning": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 0.20 * 1e-6,
        "price_per_completion_tokens": 0.50 * 1e-6,
        "context_length": 2000000,
        "max_tokens": 256000,
        "client_config": {
            "api_key_env": "GROK_API_KEY",
            "base_url": "https://api.x.ai/v1",
            "client_class": "Grok"
        }
    },
    "grok-4-1-fast-non-reasoning": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 0.20 * 1e-6,
        "price_per_completion_tokens": 0.50 * 1e-6,
        "context_length": 2000000,
        "max_tokens": 256000,
        "client_config": {
            "api_key_env": "GROK_API_KEY",
            "base_url": "https://api.x.ai/v1",
            "client_class": "Grok"
        }
    },
    "grok-4-1-fast-reasoning": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 0.20 * 1e-6,
        "price_per_completion_tokens": 0.50 * 1e-6,
        "context_length": 2000000,
        "max_tokens": 256000,
        "client_config": {
            "api_key_env": "GROK_API_KEY",
            "base_url": "https://api.x.ai/v1",
            "client_class": "Grok"
        }
    },
    "claude-haiku-4-5": {
        "structured_output": False,
        "vision": True,
        "price_per_prompt_tokens": 1.00 * 1e-6,
        "price_per_completion_tokens": 5.00 * 1e-6,
        "context_length": 200000,
        "max_tokens": 64000,
        "client_config": {
            "api_key_env": "ANTHROPIC_API_KEY",
            "base_url": "https://api.anthropic.com/v1",
            "client_class": "Anthropic"
        }
    },
    "claude-haiku-4-5-thinking": {
        "structured_output": False,
        "vision": True,
        "price_per_prompt_tokens": 1.00 * 1e-6,
        "price_per_completion_tokens": 5.00 * 1e-6,
        "context_length": 200000,
        "max_tokens": 64000,
        "thinking": {
            "type": "enabled",
            "budget_tokens": 4096
        },
        "client_config": {
            "api_key_env": "ANTHROPIC_API_KEY",
            "base_url": "https://api.anthropic.com/v1",
            "client_class": "Anthropic"
        }
    },
    "claude-sonnet-4-5-thinking": {
        "structured_output": False,
        "vision": True,
        "price_per_prompt_tokens": 3.00 * 1e-6,
        "price_per_completion_tokens": 15.00 * 1e-6,
        "context_length": 200000,
        "max_tokens": 64000,
        "thinking": {
            "type": "enabled",
            "budget_tokens": 4096
        },
        "client_config": {
            "api_key_env": "ANTHROPIC_API_KEY",
            "base_url": "https://api.anthropic.com/v1",
            "client_class": "Anthropic"
        }
    },
    "claude-opus-4-5": {
        "structured_output": False,
        "vision": True,
        "price_per_prompt_tokens": 5.00 * 1e-6,
        "price_per_completion_tokens": 25.00 * 1e-6,
        "context_length": 200000,
        "max_tokens": 64000,
        "client_config": {
            "api_key_env": "ANTHROPIC_API_KEY",
            "base_url": "https://api.anthropic.com/v1",
            "client_class": "Anthropic"
        }
    },
    "claude-opus-4-5-thinking": {
        "structured_output": False,
        "vision": True,
        "price_per_prompt_tokens": 5.00 * 1e-6,
        "price_per_completion_tokens": 25.00 * 1e-6,
        "context_length": 200000,
        "max_tokens": 64000,
        "thinking": {
            "type": "enabled",
            "budget_tokens": 4096
        },
        "client_config": {
            "api_key_env": "ANTHROPIC_API_KEY",
            "base_url": "https://api.anthropic.com/v1",
            "client_class": "Anthropic"
        }
    },
    "claude-sonnet-4-5": {
        "structured_output": False,
        "vision": True,
        "price_per_prompt_tokens": 3.00 * 1e-6,
        "price_per_completion_tokens": 15.00 * 1e-6,
        "context_length": 200000,
        "max_tokens": 64000,
        "client_config": {
            "api_key_env": "ANTHROPIC_API_KEY",
            "base_url": "https://api.anthropic.com/v1",
            "client_class": "Anthropic"
        }
    },
    "claude-sonnet-4-0": {
        "structured_output": False,
        "vision": True,
        "price_per_prompt_tokens": 3.00 * 1e-6,
        "price_per_completion_tokens": 15.00 * 1e-6,
        "context_length": 200000,
        "max_tokens": 64000,
        "client_config": {
            "api_key_env": "ANTHROPIC_API_KEY",
            "base_url": "https://api.anthropic.com/v1",
            "client_class": "Anthropic"
        }
    },
    "claude-sonnet-4-0-thinking": {
        "structured_output": False,
        "vision": True,
        "price_per_prompt_tokens": 3.00 * 1e-6,
        "price_per_completion_tokens": 15.00 * 1e-6,
        "context_length": 200000,
        "max_tokens": 64000,
        "thinking": {
            "type": "enabled",
            "budget_tokens": 4096
        },
        "client_config": {
            "api_key_env": "ANTHROPIC_API_KEY",
            "base_url": "https://api.anthropic.com/v1",
            "client_class": "Anthropic"
        }
    },
    "claude-3-7-sonnet-latest-thinking": {
        "structured_output": False,
        "vision": True,
        "price_per_prompt_tokens": 3.00 * 1e-6,
        "price_per_completion_tokens": 15.00 * 1e-6,
        "context_length": 200000,
        "max_tokens": 64000,
        "thinking": {
            "type": "enabled",
            "budget_tokens": 8000
        },
        "client_config": {
            "api_key_env": "ANTHROPIC_API_KEY",
            "base_url": "https://api.anthropic.com/v1",
            "client_class": "Anthropic"
        }
    },
    "claude-3-7-sonnet-latest": {
        "structured_output": False,
        "vision": True,
        "price_per_prompt_tokens": 3.00 * 1e-6,
        "price_per_completion_tokens": 15.00 * 1e-6,
        "context_length": 200000,
        "max_tokens": 64000,
        "client_config": {
            "api_key_env": "ANTHROPIC_API_KEY",
            "base_url": "https://api.anthropic.com/v1",
            "client_class": "Anthropic"
        }
    },
    "gemini-2.0-flash": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 0.10 * 1e-6, # (text / image / video)
        "price_per_completion_tokens": 0.40 * 1e-6, 
        "context_length": 500000,
        "max_tokens": 500000,
        "client_config": {
            "api_key_env": "GEMINI_API_KEY",
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "client_class": "Google"
        }
    }, 
    "gemini-2.5-flash": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 0.3 * 1e-6, # (text / image / video)
        "price_per_completion_tokens": 2.50 * 1e-6, 
        "context_length": 1000000,
        "max_tokens": 65000,
        "client_config": {
            "api_key_env": "GEMINI_API_KEY",
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "client_class": "Google"
        }
    },
    "gemini-flash-latest": {    # latest version of gemini-flash, point to gemini-2.5-flash-preview-09-2025
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 0.3 * 1e-6, # (text / image / video)
        "price_per_completion_tokens": 2.50 * 1e-6, 
        "context_length": 1000000,
        "max_tokens": 65000,
        "client_config": {
            "api_key_env": "GEMINI_API_KEY",
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "client_class": "Google"
        }
    },
    "gemini-2.5-pro": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 1.25 * 1e-6, # (text / image / video)
        "price_per_completion_tokens": 10.00 * 1e-6, 
        "context_length": 1000000,
        "max_tokens": 65000,
        "client_config": {
            "api_key_env": "GEMINI_API_KEY",
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "client_class": "Google"
        }
    },
    "gemini-3-pro-preview": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 2.00 * 1e-6, # (text / image / video)
        "price_per_completion_tokens": 12.00 * 1e-6, 
        "context_length": 1000000,
        "max_tokens": 65000,
        "client_config": {
            "api_key_env": "GEMINI_API_KEY",
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "client_class": "Google"
        }
    },
    "gemini-2.5-flash-lite": {
        "structured_output": True,
        "vision": True,
        "price_per_prompt_tokens": 0.1 * 1e-6, # (text / image / video)
        "price_per_completion_tokens": 0.40 * 1e-6,
        "context_length": 1000000,
        "max_tokens": 65536,
        "client_config": {
            "api_key_env": "GEMINI_API_KEY",
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "client_class": "Google"
        }
    },
}

class QuerySchema(BaseModel):
    query: str

class SearchSchema(BaseModel):
    result: str
    sources: list[str]

class SimpleLogger:
    """Simple colored logger with 4 methods: info, warning, data, error"""
    
    # ANSI color codes
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
    
    def __init__(self, prefix="LLMProxy", verbose=1):
        self.prefix = prefix
        self.verbose = verbose
    
    def success(self, message):
        """Log success messages in green"""
        if self.verbose >= 1:
            print(f"{self.GREEN}{self.prefix} SUCCESS: {message}{self.RESET}")
    
    def info(self, message):
        """Log info messages in light blue"""
        if self.verbose >= 1:
            print(f"{self.CYAN}{self.prefix} {message}{self.RESET}")
    
    def warning(self, message):
        """Log warning messages in yellow"""
        if self.verbose >= 1:
            print(f"{self.YELLOW}{self.prefix} WARNING: {message}{self.RESET}")
    
    def data(self, message):
        """Log data messages in purple"""
        if self.verbose >= 2:
            print(f"{self.PURPLE}{self.prefix} {message}{self.RESET}")
    
    def error(self, message):
        """Log error messages in red"""
        print(f"{self.RED}{self.prefix} ERROR: {message}{self.RESET}")

class LLMProxy:

    def __init__(self, verbose=1, api_key: Optional[str] = None, enable_timeouts= False, timeouts_options= None):
        
        # Create simple colored logger
        self.logger = SimpleLogger(verbose)
        
        # Set up timeout configuration
        if enable_timeouts and timeouts_options is None:
            timeouts_options = {"total": 120, "read": 60.0, "write": 60.0, "connect": 10.0}
        self.timeout_config = httpx.Timeout(
            timeouts_options["total"],
            read=timeouts_options["read"],
            write=timeouts_options["write"],
            connect=timeouts_options["connect"]
        ) if enable_timeouts else None
        
        # Initialize OpenAI client
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            self.logger.warning("OpenAI API key not found. Using placeholder for now. Please set OPENAI_API_KEY in your .env file.")
            openai_api_key = "placeholder-key"
        self.openai_client = OpenAI(api_key=openai_api_key,
            timeout=self.timeout_config if enable_timeouts else None
        )
        self.default_openai_base_url = "https://api.openai.com/v1"
        
        # Initialize Anthropic client
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if not anthropic_api_key:
            self.logger.warning("Anthropic API key not found. Using placeholder for now. Please set ANTHROPIC_API_KEY in your .env file.")
            anthropic_api_key = "placeholder-key"
        self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
        
        # Initialize Groq client
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            self.logger.warning("Groq API key not found. Using placeholder for now. Please set GROQ_API_KEY in your .env file.")
            groq_api_key = "placeholder-key"
        self.groq_client = Groq(api_key=groq_api_key)
        
        # Initialize Google client
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            self.logger.warning("Gemini API key not found. Using placeholder for now. Please set GEMINI_API_KEY in your .env file.")
            gemini_api_key = "placeholder-key"
        self.google_client = google_client(api_key=gemini_api_key)
        
        # Initialize Grok client
        grok_api_key = os.getenv("GROK_API_KEY")
        if not grok_api_key:
            self.logger.warning("Grok API key not found. Using placeholder for now. Please set GROK_API_KEY in your .env file.")
            grok_api_key = "placeholder-key"
        self.grok_client = grok_client(api_key=grok_api_key)
        
        # Initialize DeepSeek client
        deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        if not deepseek_api_key:
            self.logger.warning("DeepSeek API key not found. Using placeholder for now. Please set DEEPSEEK_API_KEY in your .env file.")
            deepseek_api_key = "placeholder-key"
        self.deepseek_client = OpenAI(base_url="https://api.deepseek.com", api_key=deepseek_api_key)
        
        # Initialize Qwen client
        qwen_api_key = os.getenv("QWEN_API_KEY")
        if not qwen_api_key:
            self.logger.warning("Qwen API key not found. Using placeholder for now. Please set QWEN_API_KEY in your .env file.")
            qwen_api_key = "placeholder-key"
        self.qwen_client = OpenAI(base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1", api_key=qwen_api_key)
        
        # Initialize Exa client
        exa_key = os.getenv("EXA_API_KEY")
        if not exa_key:
            self.logger.warning("Exa API key not found. Using placeholder for now. Please set EXA_API_KEY in your .env file.")
            exa_key = "placeholder-key"
        self.exa_key = exa_key

        self.exa_client = Exa(api_key=exa_key)

        # Initialize SERP API key
        serp_api_key = os.getenv("SERP_API_KEY")
        if not serp_api_key:
            self.logger.warning("SERP API key not found. Using placeholder for now. Please set SERP_API_KEY in your .env file.")
            serp_api_key = "placeholder-key"
        self.serp_api_key = serp_api_key
        
        # Initialize Ollama client
        ollama_api_key = os.getenv("OLLAMA_API_KEY", "ollama")  # Local Ollama doesn't require a real API key
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        self.ollama_client = OpenAI(
            api_key=ollama_api_key,
            base_url=ollama_base_url,
            timeout=self.timeout_config if enable_timeouts else None
        )
        
        # Cache for clients with custom base URLs
        self._client_cache = {}

        # Map provider names to client and response function
        self._provider_map = {
            "OpenAI": {"client":self.openai_client, "response_function":self.openai_response},
            "Anthropic": {"client":self.anthropic_client, "response_function":self.claude_response},
            "Groq": {"client":self.groq_client, "response_function":self.groq_response},
            "Google": {"client":self.google_client, "response_function":self.gemini_response},
            "DeepSeek": {"client":self.deepseek_client, "response_function":self.deepseek_response},
            "Alibaba": {"client":self.qwen_client, "response_function":self.qwen_response},
            "Grok": {"client":self.grok_client, "response_function":self.grok_response},
            "Ollama": {"client":self.ollama_client, "response_function":self.ollama_response},
        }

        self.best_model = {
            "OpenAI": "chatgpt-4o-latest",
            "Anthropic": "claude-sonnet-4-0",
            "Groq": "moonshotai/kimi-k2-instruct",
            "Google": "gemini-2.5-pro",
            "DeepSeek": "deepseek-reasoner",
            "Alibaba": "qwen-max-latest",
            "Grok": "grok-4-latest",
            "Ollama": "ollama/qwen3:4b",  # Not used for fallback (Ollama has fallbacks disabled)
        }

        self.fast_model = {
            "OpenAI": "gpt-4.1-nano",
            "Anthropic": "claude-sonnet-4-0",
            "Groq": "meta-llama/llama-4-scout-17b-16e-instruct",
            "Google": "gemini-2.5-flash-lite",
            "DeepSeek": "deepseek-chat",
            "Alibaba": "qwen-flash",
            "Grok": "grok-3-mini-latest",
            "Ollama": "gemini-2.5-flash-lite",
        }

        self.default_vision_models = {
            "OpenAI": "gpt-4.1-mini",
            "Anthropic": "claude-3-7-sonnet-latest",
            "Groq": "meta-llama/llama-4-maverick-17b-128e-instruct",
            "Google": "gemini-2.5-flash",
            "DeepSeek": "gemini-2.5-flash",
            "Alibaba": "gemini-2.5-flash",
            "Grok": "grok-4-latest",
            "Ollama": "gemini-2.5-flash",
        }

        #self.schema_modification_model = "moonshotai/kimi-k2-instruct"
        self.structured_output_fallback_model = "chatgpt-4o-latest"
        self.fallback_to_provider_best_model = True
        self.fallback_to_standard_model = True

        """# load guidelines.txt
        with open("guidelines.txt", "r") as f:
            self.guidelines = f.read()"""

        self.json_instructions = """
        Make sure your output is a valid JSON object as per the schema.
        Do not produce a schema, provide a json object that adheres to the pydantic schema and can be parsed into a python dict.
        Do not include any additional text outside the json format.
        Also do not use json markers and backticks like ```json and ```
        This is important because your output will be automatically parsed.
        """
    
    def get_model_config(self, model_name: str):
        """Return model configuration, supporting dynamic providers such as Ollama."""
        if model_name in MODEL_CONFIGS:
            return MODEL_CONFIGS[model_name]

        if model_name.startswith("ollama/"):
            engine_model = model_name.split("/", 1)[1]
            return {
                "structured_output": True,
                "vision": False,
                "price_per_prompt_tokens": 0.0,
                "price_per_completion_tokens": 0.0,
                "context_length": 1_000_000,
                "max_tokens": 100_000,
                "client_config": {
                    "api_key_env": "OLLAMA_API_KEY",
                    "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
                    "client_class": "Ollama"
                },
                "engine_model_name": engine_model
            }

        raise ValueError(f"Unsupported model: {model_name}")

    def get_client_for_model(self, model_name: str, model_config: dict):
        """Return an API client instance for the given model, honoring custom base URLs."""
        client_cfg = model_config["client_config"]
        provider = client_cfg["client_class"]
        base_url = client_cfg.get("base_url")

        if provider != "OpenAI":
            if provider not in self._provider_map:
                raise ValueError(f"Unknown provider '{provider}' for model '{model_name}'. Available providers: {list(self._provider_map.keys())}")
            return self._provider_map[provider]["client"]

        if not base_url or base_url == self.default_openai_base_url:
            return self.openai_client

        cache_key = (provider, base_url)
        if cache_key in self._client_cache:
            return self._client_cache[cache_key]

        api_key_env = client_cfg.get("api_key_env", "OPENAI_API_KEY")
        api_key = os.getenv(api_key_env)
        if not api_key:
            self.logger.warning(f"{provider} API key not found for {model_name}. Using placeholder. Please set {api_key_env} if required.")
            api_key = "placeholder-key"

        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=self.timeout_config
        )
        self._client_cache[cache_key] = client
        return client

    def generate_query(self, user_input, model_name):
        system_prompt = """
        You are a helpful assistant.
        Your task is to generate a query for a search engine, given a user input.
        """
        schema = QuerySchema
        model_config = self.get_model_config(model_name)
        client = model_config["client_config"]["client_class"]
        model_name = self.fast_model[client]
        user_prompt = f"User Input:\n{user_input}\n\nGenerate a suitable query for a search engine:\n"
        try:
            response, execution_time, token_usage, price = self.ask_llm(model_name=model_name, system_prompt=system_prompt, user_prompt=user_prompt, schema=schema)
            response = json.loads(response)
            return response["query"], token_usage, price
        except Exception as e:
            self.logger.error(f"[LLMProxy] Query generation failed using model '{model_name}'. Ensure API keys are configured. Error: {e}")
            raise

    def describe_image(self, image_path, model_name):
        """
        Describe image content for models that don't support vision.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            str: Detailed description of the image content
        """
        self.logger.info(f"[LLMProxy] Using fallback for image description...")
        
        system_prompt = """
        You are a computer vision expert. Provide a detailed, accurate description of the image.
        Focus on objects, text, colors, scene context, and any relevant details that would be useful for analysis.
        """
        
        user_prompt = f"Describe this image in detail, including any text, objects, colors, and context."
        
        model_config = self.get_model_config(model_name)
        provider = model_config["client_config"]["client_class"]
        model_name = self.default_vision_models[provider]
        
        try:
            response, execution_time, token_usage, price = self.ask_llm(model_name=model_name, system_prompt=system_prompt, user_prompt=user_prompt, image_path=image_path)
                
            self.logger.info(f"[LLMProxy] Image description:\n{response}")
            
            return response, token_usage, price
            
        except Exception as e:
            self.logger.error(f"[LLMProxy] Vision fallback failed using model '{model_name}'. Ensure API keys are configured. Error: {e}")
            return f"Error describing image: {str(e)}", {}, 0

    def ask_llm(self, model_name="gpt-4o-mini", 
                system_prompt="", 
                user_prompt="",
                temperature=None,
                schema=None,
                image_path=None,
                file_path=None,
                websearch=False,
                use_query_generator=False,
                max_search_results=12,
                search_tool="exa", # exa, serp, both (exa + serp)
                max_tokens=None,
                fallback_to_provider_best_model=True,
                fallback_to_standard_model=True,
                retry_limit=1):
        """
        Makes a request to the model using the specified parameters.

        :param model_name: The name of the model to use. Default is 'gpt-4o-mini'.
        :param system_prompt: The system prompt for the model. Default is an empty string.
        :param user_prompt: The user prompt for the model. Default is an empty string.
        :param temperature: Controls randomness in the response. Default is 0.7.
        :param schema: The schema for the structured response. Default is None.
        :param image_path: Path to an image file to be used as input. Default is None.
        :param file_path: Path to a file to be used as input. Default is None.
        :param websearch: Whether to perform a web search. Default is False.
        :param use_query_generator: Whether to use query generator. Default is False.
        :param max_search_results: Maximum number of search results to return. Default is 12.
        :param search_tool: Whether to use exa, serp or both (exa + serp). Default is exa.
        :param fallback_to_provider_best_model: Whether to fallback to provider best model. Default is True.
        :param fallback_to_standard_model: Whether to fallback to standard model. Default is True.
        :param retry_limit: The number of times to retry the request if an exception occurs.

        :return: A tuple containing:
                - response: The API response object
                - execution_time: Time taken to execute the request in seconds
                - token_usage: Dictionary containing token usage information
                - price: Calculated price for the request
        :raises: ValueError if model is not supported
                Exception for API errors after retry limit is reached
        """
        start_time = time.time()
        retry_count = 0
        last_error = None

        self.fallback_to_provider_best_model = fallback_to_provider_best_model
        self.fallback_to_standard_model = fallback_to_standard_model
        
        if websearch and not schema:
            schema = SearchSchema

        # Get model configuration
        model_config = self.get_model_config(model_name)
        
        if max_tokens and max_tokens>model_config["max_tokens"]:
            self.logger.warning(f"[ask_llm] The specified max tokens exceeds model limit, setting max_tokens to default")
            max_tokens = None
        
        # Handle vision fallback for models that don't support vision
        if image_path and not model_config["vision"]:
            self.logger.warning(f"[LLMProxy] Model {model_name} doesn't support vision, using fallback...")
            image_description, image_token_usage, image_price = self.describe_image(image_path, model_name)
            user_prompt = f"{user_prompt}\n\nImage Description (provided by fallback):\n{image_description}"
            image_path = None  # Prevent passing image to non-vision model
        
        if file_path:
            provider_name = model_config["client_config"]["client_class"]
            needs_manual_embedding = provider_name in ["Groq", "Grok", "DeepSeek", "Qwen", "Ollama"]
            if needs_manual_embedding:
                try:
                    file_contents = self.read_file_content(file_path)
                    user_prompt = f"{user_prompt}\nDocument Content: {file_contents}"
                    if provider_name == "Ollama":
                        self.logger.warning("[LLMProxy] Ollama models do not support direct file uploads. Inlining file content into the prompt.")
                        file_path = None
                except Exception as exc:
                    self.logger.error(f"[LLMProxy] Failed to read file {file_path}: {exc}")
                    raise

        if websearch:
            self.logger.info("[ask_llm] Using web search...")
            if use_query_generator:
                self.logger.info(f"[ask_llm] Generating Search Query...")
                search_query, query_token_usage, query_price = self.generate_query(user_input=user_prompt, model_name=model_name)
                self.logger.info(f"[ask_llm] Search Query: {search_query}")
            else:
                search_query = user_prompt
                query_token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                query_price = 0
            
            if search_tool == "exa":
                search_results, search_cost = self.search_web_with_exa(
                    search_query,
                    max_results=max_search_results
                )
            elif search_tool == "serp":
                search_results, search_cost = self.search_web_with_serp(
                    search_query,
                    max_results=max_search_results
                )
            else: # search_tool == "both"   
                search_results_exa, search_cost_exa = self.search_web_with_exa(
                    search_query,
                    max_results=max_search_results
                )
                search_results_serp, search_cost_serp = self.search_web_with_serp(
                    search_query,
                    max_results=max_search_results
                )
                search_results = f">> EXA Search Results:\n{search_results_exa}\n\n\n>> SERP Search Results:\n{search_results_serp}"
                search_cost = search_cost_exa + search_cost_serp
            user_prompt = f"{user_prompt}\n\nRelevant Information from {search_tool.upper()} Web Search:\n{search_results}"

        # Extract pricing information
        price_per_prompt_tokens = model_config["price_per_prompt_tokens"]
        price_per_completion_tokens = model_config["price_per_completion_tokens"]

        # Print parameters for debugging
        self.logger.info(f"[ask_llm] Model Name: {model_name}")
        self.logger.info(f"[ask_llm] Temperature: {temperature}")
        self.logger.info(f"[ask_llm] Schema: {True if schema else False}")
        self.logger.info(f"[ask_llm] Max Tokens: {max_tokens}")
        self.logger.info(f"[ask_llm] Vision: {True if image_path else False}")
        self.logger.info(f"[ask_llm] File: {True if file_path else False}")
        self.logger.info(f"[ask_llm] Websearch: {websearch}")
        if websearch:
            self.logger.info(f"[ask_llm] Use Query Generator: {use_query_generator}")
            self.logger.info(f"[ask_llm] Max Search Results: {max_search_results}")
            self.logger.info(f"[ask_llm] Search Tool: {search_tool}")
        self.logger.info(f"[ask_llm] Retry Limit: {retry_limit}")

        while retry_count < retry_limit:
            try:
                provider = model_config["client_config"]["client_class"]
                response_function = self._provider_map[provider]["response_function"]
                client = self.get_client_for_model(model_name, model_config)
                
                # Generate response with fallback logic
                response, token_usage = self._generate_response_with_fallbacks(
                    client, response_function, model_name, system_prompt, user_prompt, 
                    schema, temperature, provider, image_path, file_path, max_tokens
                )

                end_time = time.time()
                execution_time = end_time - start_time

                # Calculate price based on token usage
                price = (token_usage["prompt_tokens"] * price_per_prompt_tokens + 
                        token_usage["completion_tokens"] * price_per_completion_tokens)
                if "query_price" in locals():
                    price += query_price
                
                if "image_price" in locals():
                    price += image_price
                
                if "search_cost" in locals():
                    price += search_cost
                
                if "query_token_usage" in locals():
                    token_usage["prompt_tokens"] += query_token_usage["prompt_tokens"]
                    token_usage["completion_tokens"] += query_token_usage["completion_tokens"]
                    token_usage["total_tokens"] += query_token_usage["total_tokens"]
                
                if "image_token_usage" in locals():
                    token_usage["prompt_tokens"] += image_token_usage["prompt_tokens"]
                    token_usage["completion_tokens"] += image_token_usage["completion_tokens"]
                    token_usage["total_tokens"] += image_token_usage["total_tokens"]
                
                self.logger.success("SUCCESS")
                self.logger.data(f"Response:\n{response}")
                self.logger.success(f"Execution Time: {execution_time:.2f} seconds")
                self.logger.success(f"Token Usage:\n{json.dumps(token_usage, indent=2)}")
                self.logger.success(f"Price: {price:.4f} USD")
                
                return response, execution_time, token_usage, price

            except Exception as e:
                last_error = e
                self.logger.error(f"[LLMProxy] Exception: {e}")
                self.logger.warning(f'Failed to generate response ({retry_count}/{retry_limit}). Retrying...')
                if retry_count == retry_limit-1:
                    self.logger.error(traceback.format_exc())
                retry_count += 1
                time.sleep(2)
                if retry_count >= retry_limit:
                    break
            
        # If we've exhausted all retries, raise the last error with context
        error_msg = f"[LLMProxy] Gave up after {retry_limit} attempts. Last error: {str(last_error)}"
        self.logger.error(error_msg)
        raise Exception(error_msg)

    def _generate_response_with_fallbacks(self, client, response_function, model_name, 
                                        system_prompt, user_prompt, schema, temperature, provider, image_path, file_path, max_tokens):
        """
        Generate response with structured fallback logic for validation failures.
        """
        if schema is None:
            return self._generate_unstructured_response(
                client, response_function, model_name, system_prompt, user_prompt, temperature, image_path, file_path, max_tokens
            )
        
        model_config = self.get_model_config(model_name)
        if model_config["structured_output"]:
            return self._generate_structured_response(
                client, response_function, model_name, system_prompt, user_prompt, 
                schema, temperature, provider, image_path, file_path, max_tokens
            )
        else:
            return self._generate_pseudo_structured_response(
                client, response_function, model_name, system_prompt, user_prompt, 
                schema, temperature, provider, image_path, file_path, max_tokens
            )

    def _generate_unstructured_response(self, client, response_function, model_name, 
                                    system_prompt, user_prompt, temperature, image_path, file_path, max_tokens):
        """Generate response without schema validation."""
        self.logger.info(f"[LLMProxy] Generating unstructured output...")
        response, token_usage = response_function(
            client, model_name, system_prompt, user_prompt, temperature=temperature, image_path=image_path, file_path=file_path, max_tokens=max_tokens
        )
        #self.logger.info(f"RESPONSE:\n{response}")
        return response, token_usage

    def _generate_structured_response(self, client, response_function, model_name, 
                                    system_prompt, user_prompt, schema, temperature, provider, image_path, file_path, max_tokens):
        """Generate response with native structured output support."""
        self.logger.info(f"[LLMProxy] Generating structured output...")
        fallback_models = [model_name]
        allow_fallbacks = provider != "Ollama"

        if not allow_fallbacks and (self.fallback_to_provider_best_model or self.fallback_to_standard_model):
            self.logger.warning("[LLMProxy] Fallbacks are disabled for Ollama models. Ignoring fallback settings.")

        if allow_fallbacks and self.fallback_to_provider_best_model:
            fallback_models.append(self.best_model[provider])
        
        if allow_fallbacks and self.fallback_to_standard_model:
            fallback_models.append(self.structured_output_fallback_model)
        
        for i, current_model in enumerate(fallback_models):
            try:
                # Get the correct client and response function for the current model
                if i < 2:
                    current_client = client
                    current_response_function = response_function
                else:
                    # For fallback model, get the correct provider and response function
                    current_client = self.openai_client
                    fallback_provider = MODEL_CONFIGS[self.structured_output_fallback_model]["client_config"]["client_class"]
                    current_response_function = self._provider_map[fallback_provider]["response_function"]
                
                response, token_usage = current_response_function(
                    current_client, current_model, system_prompt, user_prompt, 
                    schema, temperature=temperature, image_path=image_path, file_path=file_path, max_tokens=max_tokens
                )
                #self.logger.info(f"RESPONSE:\n{response}")
                schema.model_validate_json(response)
                self.logger.success(f"[LLMProxy] Pydantic validation successful")
                return response, token_usage
                
            except Exception as e:
                self._log_validation_error(e, current_model, i, fallback_models)
                self.logger.error(traceback.format_exc())
                if i == len(fallback_models) - 1:  # Last attempt failed
                    self.logger.error("Failed to validate response.")
                    raise
        
    def _generate_pseudo_structured_response(self, client, response_function, model_name, 
                                    system_prompt, user_prompt, schema, temperature, provider, image_path, file_path, max_tokens):
        """Generate response for models without native structured output."""
        self.logger.info(f"[LLMProxy] Generating pseudo-structured output...")
        self.logger.warning(f"Model {model_name} does not natively support structured responses. Exact schema not guaranteed.")
        
        fallback_models = [model_name]
        allow_fallbacks = provider != "Ollama"

        if not allow_fallbacks and (self.fallback_to_provider_best_model or self.fallback_to_standard_model):
            self.logger.warning("[LLMProxy] Fallbacks are disabled for Ollama models. Ignoring fallback settings.")

        if allow_fallbacks and self.fallback_to_provider_best_model:
            fallback_models.append(self.best_model[provider])
        
        if allow_fallbacks and self.fallback_to_standard_model:
            fallback_models.append(self.structured_output_fallback_model)
        
        modified_system_prompt = self.prompt_with_structure(system_prompt, schema)
        
        for i, current_model in enumerate(fallback_models):
            try:
                # Get the correct client and response function for the current model
                if i < 2:
                    current_client = client
                    current_response_function = response_function
                else:
                    # For fallback model, get the correct provider and response function
                    current_client = self.openai_client
                    fallback_provider = MODEL_CONFIGS[self.structured_output_fallback_model]["client_config"]["client_class"]
                    current_response_function = self._provider_map[fallback_provider]["response_function"]
                
                response, token_usage = current_response_function(
                    current_client, current_model, modified_system_prompt, user_prompt, 
                    temperature=temperature, image_path=image_path, file_path=file_path, max_tokens=max_tokens
                )
                #self.logger.info(f"RESPONSE:\n{response}")
                cleaned_response = response.replace("```json", "").replace("```", "")
                schema.model_validate_json(cleaned_response)
                self.logger.success(f"[LLMProxy] Pydantic validation successful")
                return cleaned_response, token_usage
                
            except Exception as e:
                self._log_validation_error(e, current_model, i, fallback_models)
                if i == len(fallback_models) - 1:  # Last attempt failed
                    self.logger.error("Failed to validate response.")
                    raise

    def _log_validation_error(self, error, model_name, attempt_index, fallback_models):
        """Log validation errors with appropriate fallback messaging."""
        self.logger.error(f"[LLMProxy] Pydantic validation error with model {model_name}:\n{error}")
        
        if attempt_index == 0 and len(fallback_models) > 1:
            next_model = fallback_models[1]
            self.logger.warning(f"Will attempt with a different model from the same provider: {next_model}")
        elif attempt_index == 1 and len(fallback_models) > 2:
            self.logger.warning(f"Will attempt with {self.structured_output_fallback_model}")
        else:
            self.logger.error(f"[LLMProxy] Pydantic validation error with model {model_name}: {error}")
            self.logger.error(traceback.format_exc())
    
    def prompt_with_structure(self, system_prompt, schema):
        return system_prompt + "\n\nFormat your response as a JSON object:\n\n"+json.dumps(schema.model_json_schema(), indent=2) + "\n\n" + self.json_instructions
    
    def create_image_openai(self, file_path):
        with open(file_path, "rb") as file_content:
            result = self.openai_client.files.create(
                file=file_content,
                purpose="vision",
            )
            return result.id
    
    def create_file_openai(self, file_path):
        with open(file_path, "rb") as file_content:
            result = self.openai_client.files.create(
                file=file_content,
                purpose="user_data",
            )
            return result.id
    
    def encode_image(self,image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def ollama_response(self, client, model, system_prompt, user_prompt, schema=None, temperature=None, image_path=None, file_path=None, max_tokens=None):
        """
        Handle Ollama model responses using OpenAI-compatible chat completions API.
        
        Note: File and image inputs are handled upstream in ask_llm via content inlining
        and vision fallback, so file_path and image_path will typically be None here.
        """
        # Extract the actual model name (e.g., "llama3" from "ollama/llama3")
        engine_model = model.split("/", 1)[1] if model.startswith("ollama/") else model
        
        if image_path:
            self.logger.warning(f"[LLMProxy] Ollama models do not support direct image inputs. Image should have been handled via vision fallback upstream.")
        
        if file_path:
            self.logger.warning(f"[LLMProxy] Ollama models do not support direct file inputs. File should have been inlined upstream.")
        
        # Build messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        
        # Build request parameters
        chat_kwargs = {
            "model": engine_model,
            "messages": messages,
        }
        if temperature is not None:
            chat_kwargs["temperature"] = temperature
        if max_tokens is not None:
            chat_kwargs["max_tokens"] = max_tokens
        if schema is not None:
            chat_kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": schema.__name__,
                    "schema": schema.model_json_schema(),
                },
            }
        
        # Make request
        response = client.chat.completions.create(**chat_kwargs)
        
        # Extract text
        message_content = response.choices[0].message.content
        if isinstance(message_content, list):
            text = ''.join(
                part.get("text", "") if isinstance(part, dict) else str(part)
                for part in message_content
            )
        else:
            text = message_content or ""
        
        # Validate structured output if schema provided
        if schema is not None:
            try:
                parsed = schema.model_validate_json(text)
                text = parsed.model_dump_json(indent=2)
            except Exception as exc:
                self.logger.error(f"[LLMProxy] Failed to validate Ollama structured response: {exc}")
                raise
        
        # Extract token usage safely
        usage = response.usage
        def _usage_value(obj, name):
            if obj is None:
                return 0
            if isinstance(obj, dict):
                return obj.get(name, 0)
            return getattr(obj, name, 0)
        
        token_usage = {
            "prompt_tokens": _usage_value(usage, "prompt_tokens"),
            "completion_tokens": _usage_value(usage, "completion_tokens"),
            "total_tokens": _usage_value(usage, "total_tokens"),
        }
        
        return text, token_usage

    def openai_response(self, client, model, system_prompt, user_prompt, schema=None, temperature=None, image_path=None, file_path=None, max_tokens=None):
        # All models reaching this function should be in MODEL_CONFIGS
        # (Ollama now has its own ollama_response function)
        model_cfg = MODEL_CONFIGS.get(model)
        
        user_content = [
            {"type": "input_text", "text": user_prompt}
        ]
        if image_path:
            user_content.append({
                "type": "input_image",
                "file_id": self.create_image_openai(image_path)
            })
        if file_path:
            if file_path.split('.')[-1] == "pdf":
                user_content.append({
                    "type": "input_file",
                    "file_id": self.create_file_openai(file_path)
                })
            else:
                user_content.append({
                    "type": "input_text",
                    "text": self.read_file_content(file_path)
                })
        completion_params = {
            "model": model,
            "input": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
        }
        if max_tokens:
            completion_params["max_output_tokens"] = max_tokens
        if model_cfg and "reasoning_effort" in model_cfg:
            completion_params["reasoning"] = {"effort": model_cfg["reasoning_effort"]}
        elif temperature:
            completion_params["temperature"] = temperature
        if schema:
            completion_params["text_format"] = schema
            response = client.responses.parse(**completion_params)
            text = response.output[-1].content[0].parsed
            text = text.model_dump_json(indent=2)
        else:
            response = client.responses.create(**completion_params)
            text = response.output_text
        token_usage = {
            "prompt_tokens": response.usage.input_tokens,
            "completion_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
        }
        return text, token_usage

    def grok_response(self, client, model, system_prompt, user_prompt, schema=None, temperature=None, image_path=None, file_path=None, max_tokens=None):
        user_input = [user_prompt]
        if image_path:
            base64_image = self.encode_image(image_path)
            image_input = image(image_url=f"data:image/jpeg;base64,{base64_image}", detail="auto")
            user_input.append(image_input)
        if max_tokens:
            chat = client.chat.create(model=model, temperature=temperature, max_tokens=max_tokens)
        else:
            chat = client.chat.create(model=model, temperature=temperature)
        chat.append(system(system_prompt))
        chat.append(user(*user_input))
        if schema:
            response, structure = chat.parse(schema)
            text = structure.model_dump_json(indent=2)
        else:
            response = chat.sample()
            text = response.content
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        reasoning_tokens = response.usage.reasoning_tokens
        token_usage = {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "reasoning_tokens": reasoning_tokens
        }
        return text, token_usage
    
    def gemini_response(self, client, model, system_prompt, user_prompt, schema=None, temperature=None, image_path=None, file_path=None, max_tokens=None):
        prompt = system_prompt + "\n\n" + user_prompt
        completion_params = {
            "model": model,
            "contents": [prompt]
        }
        config_params = {}
        if temperature:
            config_params["temperature"] = temperature
        if max_tokens:
            config_params["maxOutputTokens"] = max_tokens
        if schema:
            config_params["response_mime_type"] = "application/json"
            config_params["response_schema"] = schema
        if image_path:
            with open(image_path, "rb") as image:
                image_bytes = image.read()
            completion_params["contents"].append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=f"image/{image_path.split('.')[-1]}"
                )
            )
        if file_path:
            if file_path.split('.')[-1] in ["pdf", "txt"]: 
                myfile = client.files.upload(file=file_path)
                completion_params["contents"].append(myfile)
            else:
                completion_params["contents"].append(f"Document Content:\n{self.read_file_content(file_path)}")
        completion_params["config"] = types.GenerateContentConfig(**config_params)
        response = client.models.generate_content(**completion_params)
        if schema:
            text = response.text #response.parsed
            if type(text) == dict:
                text = json.dumps(text, indent=2)
            elif type(text) == str:
                text = json.loads(text)
                text = json.dumps(text, indent=2)
            else:
                text = text.model_dump_json(indent=2)
        else:
            text = response.candidates[0].content.parts[0].text
        prompt_tokens = response.usage_metadata.prompt_token_count
        completion_tokens = response.usage_metadata.candidates_token_count
        total_tokens = response.usage_metadata.total_token_count
        token_usage = {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens
        }
        return text, token_usage
    
    def groq_response(self, client, model, system_prompt, user_prompt, schema=None, temperature=None, image_path=None, file_path=None, max_tokens=None):
        user_prompt = {
            "type": "text",
            "text": user_prompt
        }
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [user_prompt]}
        ]
        request_params = {
            "model": model,
            "messages": messages
        }
        if schema:
            request_params["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": schema.__name__,
                    "schema": schema.model_json_schema()
                }
            }
        if temperature:
            request_params["temperature"] = temperature
        if max_tokens:
            request_params["max_completion_tokens"] = max_tokens
        if image_path:
            base64_image = self.encode_image(image_path)
            request_params["messages"][1]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })
        response = client.chat.completions.create(**request_params)
        text = response.choices[0].message.content
        if schema:
            text = text.replace("```json", "").replace("```", "")
            text = json.loads(text)
            text = json.dumps(text, indent=2)
        usage_data = response.usage
        token_usage = {
            "prompt_tokens": usage_data.prompt_tokens,
            "completion_tokens": usage_data.completion_tokens,
            "total_tokens": usage_data.total_tokens
        }
        return text, token_usage  

    def claude_response(self, client, model, system_prompt, user_prompt, schema=None, temperature=None, image_path=None, file_path=None, max_tokens=None):
        if schema:
            self.logger.warning("[LLMProxy] Claude does not support structured responses. Exact schema not guaranteed.")
        # Clean model name and prepare prompts
        model_name = model.replace("-thinking", "")
        system_prompt = system_prompt.replace('%', 'percent')
        user_prompt = user_prompt.replace('%', 'percent')
        content = []
        content.append({
            "type": "text",
            "text": user_prompt
        })
        if image_path:
            base64_image = self.encode_image(image_path)
            media_type = f"image/{image_path.split('.')[-1]}"
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": base64_image
                }
            })
        if file_path:
            if file_path.split('.')[-1] in ['pdf','txt']:
                type_mapper = {
                    "pdf": "application/pdf",
                    "txt": "text/plain"
                }
                file = client.beta.files.upload(
                    file=(file_path, open(file_path, "rb"), type_mapper[file_path.split('.')[-1]])
                )
                content.append({
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": file.id
                    }
                })
            else:
                content.append({
                    "type": "text",
                    "text": f"\n\nDocument Content:\n{self.read_file_content(file_path)}\n\n"
                })
        # Build message parameters
        params = {
            "model": model_name,
            "system": system_prompt,
            "messages": [{"role": "user", "content": content}],
        }
        if max_tokens:
            params["max_tokens"] = max_tokens
        else:
            params["max_tokens"] = 16000 if "3-5" not in model else 8000
        if file_path:
            params["betas"]=["files-api-2025-04-14"]
        # Add conditional parameters
        if temperature:
            params["temperature"] = temperature
        if "thinking" in model:
            params["thinking"] = MODEL_CONFIGS[model]["thinking"]
            params["temperature"] = 1
        
        try:
            if file_path:
                response = client.beta.messages.create(**params)
            else:
                response = client.messages.create(**params)
            if "thinking" in model:
                text = response.content[1].text
            else:
                text = response.content[0].text
            usage = response.usage
            
            token_usage = {
                "prompt_tokens": usage.input_tokens,
                "completion_tokens": usage.output_tokens,
                "total_tokens": usage.input_tokens + usage.output_tokens
            }
            
            return text, token_usage
            
        except Exception as e:
            traceback.print_exc()
            return None, None

    def deepseek_response(self, client, model, system_prompt, user_prompt, schema=None, temperature=None, image_path=None, file_path=None, max_tokens=None):
        if image_path:
            self.logger.error("[LLMProxy] DeepSeek does not support image inputs. Image input will be ignored.")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        request_params = {
            "model": model,
            "messages": messages
        }
        if temperature:
            request_params["temperature"] = temperature
        if max_tokens:
            request_params["max_tokens"] = max_tokens
        if schema:
            messages[1]["content"] += f"\n\nFormat your response as a JSON object:\n\n{json.dumps(schema.model_json_schema(), indent=2)}"
            request_params["response_format"] = {"type": "json_object"}
        
        response = client.chat.completions.create(**request_params)
        
        text = response.choices[0].message.content
        
        if schema:
            text = text.replace("```json", "").replace("```", "")
            text = json.loads(text)
            text = json.dumps(text, indent=2)
        
        token_usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }
        
        return text, token_usage
    
    def qwen_response(self, client, model, system_prompt, user_prompt, schema=None, temperature=None, image_path=None, file_path=None, max_tokens=None):
        if image_path:
            self.logger.error("[LLMProxy] Qwen does not support image inputs. Image input will be ignored.")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        request_params = {
            "model": model,
            "messages": messages
        }
        if schema:
            request_params["messages"][1]["content"] += f"\n\nFormat your response as a JSON object:\n\n{json.dumps(schema.model_json_schema(), indent=2)}"
            request_params["response_format"] = {"type": "json_object"}
        if temperature:
            request_params["temperature"] = temperature
        if max_tokens:
            request_params["max_tokens"] = max_tokens
        response = client.chat.completions.create(**request_params)
        text = response.choices[0].message.content
        if schema:
            text = text.replace("```json", "").replace("```", "")
        token_usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }
        return text, token_usage
    
    def read_text_file(self, file_path: str) -> str:
        """Read content from a plain text file."""
        self.logger.info("Reading text file...")
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def read_docx_file(self, file_path: str) -> str:
        """Read content from a DOCX file."""
        self.logger.info("Reading DOCX file...")
        doc = Document(file_path)
        content = []
        for paragraph in doc.paragraphs:
            content.append(paragraph.text)
        return '\n'.join(content)


    def read_json_file(self, file_path: str) -> str:
        """Read content from a JSON file and return as formatted string."""
        self.logger.info("Reading JSON file...")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return json.dumps(data, indent=2)


    def extract_text_with_pymupdf(self, file_path: str) -> tuple[str, int]:
        """
        Extract text from PDF using PyMuPDF.
        Returns tuple of (text_content, page_count).
        """
        self.logger.info("Extracting text from PDF using PyMuPDF...")
        doc = pymupdf.open(file_path)
        content = []
        
        for page in doc:
            content.append(page.get_text())
        
        doc.close()
        return '\n'.join(content), len(content)

    def is_text_based_pdf(self, file_path: str, min_words_per_page: int = 20) -> bool:
        """
        Check if PDF is text-based by extracting text and checking word density.
        Returns True if it's text-based with sufficient content.
        """
        self.logger.info("Checking if PDF is text-based...")
        try:
            text_content, page_count = self.extract_text_with_pymupdf(file_path)
            
            if not text_content.strip():
                return False
            
            word_count = len(text_content.split())
            avg_words_per_page = word_count / page_count if page_count > 0 else 0
            
            self.logger.info(f"Average words per page: {avg_words_per_page}")
            return avg_words_per_page >= min_words_per_page
        except Exception:
            traceback.print_exc()
            return False


    def extract_with_gemini(self, file_path: str) -> str:
        """Extract text from file using Gemini OCR."""
        self.logger.info("Extracting text from file using Gemini OCR...")
        client = self.google_client
        uploaded_file = client.files.upload(file=file_path)
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=["extract all the text from this file.", uploaded_file],
        )
        return response.text


    def read_pdf_file(self, file_path: str) -> str:
        """
        Read content from PDF file.
        Uses PyMuPDF for text-based PDFs, Gemini OCR for image-based or sparse PDFs.
        """
        self.logger.info("Reading PDF file...")
        if self.is_text_based_pdf(file_path):
            self.logger.info("PDF is text-based.")
            text_content, _ = self.extract_text_with_pymupdf(file_path)
            return text_content
        else:
            self.logger.info("PDF is not text-based.")
            return self.extract_with_gemini(file_path)

    def read_file_content(self, file_path: str) -> str:
        """
        Main function to read content from various file types.
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            str: Extracted text content
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file type is not supported
        """
        self.logger.info("Reading file content...")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        extension = Path(file_path).suffix.lower()
        
        if extension == '.txt':
            return self.read_text_file(file_path)
        elif extension == '.docx':
            return self.read_docx_file(file_path)
        elif extension == '.json':
            return self.read_json_file(file_path)
        elif extension == '.pdf':
            return self.read_pdf_file(file_path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")

    def search_web_with_exa(self, query: str, max_results: int = 8) -> tuple:
        """
        Search the web using Exa API.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return (default: 8)
            
        Returns:
            tuple: (context, cost)
                - context: Search results including organic results, knowledge graph, and related searches
                - cost: Cost of the search in USD
            
        Raises:
            ValueError: If Exa_KEY is not configured
            requests.RequestException: If API request fails
        """
        self.logger.info(f"[search_web] Searching the web with Exa")
        result = self.exa_client.search_and_contents(
            query,
            type = "auto",
            context = True,
            num_results = max_results,
            summary = True
        )
        context = result.context
        cost = result.cost_dollars.total
        self.logger.success(f"[search_web] Exa Search completed with cost: {cost}")
        self.logger.data(f"[search_web] Exa Search results:\n{context}")
        return context, cost
    
    def search_web_with_serp(self, query: str, max_results: int = 10) -> tuple:
        """
        Search the web using SERP API (Google search engine).
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return (default: 10)
            
        Returns:
            tuple: (search_results_dict, estimated_cost)
                - search_results_dict: Raw dictionary of search results from SERP API
                - estimated_cost: Estimated cost in USD for the search operation
            
        Raises:
            ValueError: If SERP_API_KEY is not configured
            requests.RequestException: If API request fails
        """
        self.logger.info(f"[search_web] Searching the web with SERP")
        if self.serp_api_key == "placeholder-key":
            raise ValueError("SERP API key not configured. Please set SERP_API_KEY in your .env file.")
        
        
        try:
            # Configure search parameters based on engine
            search_params = {
                "q": query,
                "api_key": self.serp_api_key,
                "engine": "google",
                "num": min(max_results, 20)  # SERP API typically limits to 20 results
            }
            
            # Perform the search
            search = GoogleSearch(search_params)
            results = search.get_dict()

            results = self.format_serp_results(results)
            
            # Estimate cost (SERP API typically charges per search)
            estimated_cost = 0.015  # Approximate cost per search, adjust based on actual pricing

            self.logger.success(f"[search_web] SERP Search completed with estimated cost: {estimated_cost}\nNote: This is an estimated cost. Adjust based on plan.")
            self.logger.data(f"[search_web] SERP Search results:\n{results}")
            
            return results, estimated_cost
            
        except Exception as e:
            self.logger.error(f"[search_web_serp] Error during search: {str(e)}")
            raise requests.RequestException(f"SERP API search failed: {str(e)}")

    def format_serp_results(self, results: dict) -> str:
        """
        Format SERP search results into a readable string.
        
        Args:
            results: Raw dictionary of search results from SERP API
            
        Returns:
            str: Formatted string of search results
        """
        formatted_results = ""
        if 'organic_results' in results:
            for result in results['organic_results']:
                if 'title' in result:
                    formatted_results += f"Title: {result['title']}\n"
                if 'link' in result:
                    formatted_results += f"Link: {result['link']}\n"
                if 'snippet' in result:
                    formatted_results += f"Snippet: {result['snippet']}\n"
                formatted_results += "\n"
        if 'related_questions' in results:
            for result in results['related_questions']:
                if 'question' in result:
                    formatted_results += f"Question: {result['question']}\n"
                if 'title' in result:
                    formatted_results += f"Title: {result['title']}\n"
                if 'link' in result:
                    formatted_results += f"Link: {result['link']}\n"
                if 'snippet' in result:
                    formatted_results += f"Snippet: {result['snippet']}\n"
                formatted_results += "\n"
        return formatted_results