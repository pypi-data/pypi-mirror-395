"""
LangChain Agent Config - A library for managing multiple LangChain model configurations.

This library provides:
- Configuration management from .env files
- Validation using Pydantic
- Automatic agent creation for multiple providers (Gemini, OpenAI, Anthropic)
"""

from .config import (
    ModelConfig,
    ModelsEnv,
    read_env_file,
)

__version__ = "0.1.0"
__all__ = [
    "ModelConfig",
    "ModelsEnv",
    "read_env_file",
]

