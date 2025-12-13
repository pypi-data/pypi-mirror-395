# LangChain Agent Config

A Python library for managing multiple LangChain model configurations with validation and automatic agent creation.

## Features

- ✅ **Multi-provider support**: Gemini (Google), OpenAI (GPT), and Anthropic (Claude)
- ✅ **Robust validation**: Pydantic-based validation with custom validators
- ✅ **Environment-based configuration**: Support for multi-line `.env` files
- ✅ **Automatic agent creation**: Creates LangChain agents from configuration
- ✅ **Type-safe**: Full type hints and Pydantic models
- ✅ **Well tested**: 43+ tests with pytest

## Installation

```bash
pip install langchain-agent-config
```

## Quick Start

1. Create a `.env` file in your project root:

```env
MODELS=[
    {
        "name":"gemini",
        "model":"gemini-2.0-flash-exp",
        "temperature":0.7,
        "key":"your-google-api-key",
        "max_tokens":2048
    },
    {
        "name":"gpt",
        "model":"gpt-4",
        "temperature":0.5,
        "key":"your-openai-api-key",
        "max_tokens":4096
    }
]
```

2. Use in your code:

```python
from langchain_agent_config import ModelsEnv, read_env_file
from pathlib import Path
import json

# Load configuration
env_path = Path(".env")
env_vars = read_env_file(env_path)
raw_models = json.loads(env_vars["MODELS"])

# Validate and create models
models_env = ModelsEnv(models=raw_models)

# Create agents
agents = models_env.create_agents()

# Use the agents
response = agents['gemini'].invoke("Hello!")
response2 = agents['gpt'].invoke("Hello!")
```

## Configuration

### Model Configuration Fields

- **name** (str): Model identifier (must contain 'gemini', 'gpt'/'openai', or 'anthropic'/'claude')
- **model** (str): Specific model name from the provider
- **temperature** (float): Value between 0.0 and 1.0
- **key** (str): API key for the model provider
- **max_tokens** (int): Maximum number of tokens (must be positive)

### Supported Providers

- **Gemini**: Models with "gemini" in the name
- **OpenAI/GPT**: Models with "gpt" or "openai" in the name
- **Anthropic/Claude**: Models with "anthropic" or "claude" in the name

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=backend.model
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

