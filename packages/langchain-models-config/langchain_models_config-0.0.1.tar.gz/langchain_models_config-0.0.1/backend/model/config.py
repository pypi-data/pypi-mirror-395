import json
import os
from pathlib import Path
from typing import List, Dict, Any
from pydantic import BaseModel, ValidationError, ConfigDict, field_validator

# Import LangChain models (LangChain 1.0)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# Get the current file directory and build the path to .env
# config.py is in backend/model/, so .env is in backend/
current_dir = Path(__file__).parent
env_path = current_dir.parent / ".env"

# Read the .env file directly to support multi-line format
def read_env_file(env_path: Path) -> dict:
    """Reads the .env file and returns a dictionary with the variables"""
    env_vars = {}
    if not env_path.exists():
        return env_vars
    
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Process the file line by line
    lines = content.split('\n')
    current_key = None
    current_value = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Check if it's a new variable (KEY=VALUE format)
        if '=' in line and not line.startswith(' '):
            # Save the previous variable if it exists
            if current_key:
                env_vars[current_key] = '\n'.join(current_value).strip()
            
            # Process new variable
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            # Remove quotes if they exist
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            
            current_key = key
            current_value = [value] if value else []
        else:
            # Continuation of the previous variable (multi-line)
            if current_key:
                current_value.append(line)
    
    # Save the last variable
    if current_key:
        env_vars[current_key] = '\n'.join(current_value).strip()
    
    return env_vars

# Load variables from .env
env_vars = read_env_file(env_path)

class ModelConfig(BaseModel):
    name: str
    model: str
    temperature: float
    key: str
    max_tokens: int

    model_config = ConfigDict(extra="forbid")

    @field_validator('name', 'model', 'key', mode='before')
    @classmethod
    def strip_and_validate_string(cls, v: str) -> str:
        """Removes leading/trailing spaces and validates that it's not empty"""
        if not isinstance(v, str):
            raise ValueError("Must be a string")
        stripped = v.strip()
        if not stripped:
            raise ValueError(f"Cannot be an empty string or contain only spaces")
        return stripped

    @field_validator('temperature')
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        """Validates that temperature is between 0.0 and 1.0"""
        if not isinstance(v, (int, float)):
            raise ValueError("Temperature must be a number")
        if v < 0.0 or v > 1.0:
            raise ValueError("Temperature must be between 0.0 and 1.0")
        return float(v)

    @field_validator('max_tokens')
    @classmethod
    def validate_max_tokens(cls, v: int) -> int:
        """Validates that max_tokens is a positive integer"""
        if not isinstance(v, int):
            raise ValueError("max_tokens must be an integer")
        if v <= 0:
            raise ValueError("max_tokens must be a positive integer")
        return v


class ModelsEnv(BaseModel):
    models: List[ModelConfig]
    model_config = ConfigDict(extra="forbid")

    def create_agents(self) -> Dict[str, Any]:
        """
        Creates LangChain agents for each model configuration.
        Returns a dictionary with model names as keys and agent instances as values.
        """
        agents = {}
        
        for model_config in self.models:
            name = model_config.name.lower()
            
            # Create agent based on model name
            if "gemini" in name:
                agents[model_config.name] = ChatGoogleGenerativeAI(
                    model=model_config.model,
                    temperature=model_config.temperature,
                    max_tokens=model_config.max_tokens,
                    google_api_key=model_config.key
                )
            elif "gpt" in name or "openai" in name:
                agents[model_config.name] = ChatOpenAI(
                    model=model_config.model,
                    temperature=model_config.temperature,
                    max_tokens=model_config.max_tokens,
                    api_key=model_config.key
                )
            elif "anthropic" in name or "claude" in name:
                agents[model_config.name] = ChatAnthropic(
                    model=model_config.model,
                    temperature=model_config.temperature,
                    max_tokens=model_config.max_tokens,
                    api_key=model_config.key
                )
            else:
                raise ValueError(
                    f"Unknown model type for name '{model_config.name}'. "
                    "Supported types: 'gemini', 'gpt', 'openai', 'anthropic', 'claude'"
                )
        
        return agents


# Get MODELS from dictionary
raw_models = env_vars.get("MODELS") or env_vars.get("models")

# Only validate when running as script, not when importing
if __name__ == "__main__":
    if not raw_models:
        raise ValueError("MODELS variable not found in .env")

    try:
        parsed = json.loads(raw_models)
    except json.JSONDecodeError:
        raise ValueError("MODELS contains invalid JSON")

    try:
        validated = ModelsEnv(models=parsed)
    except ValidationError as e:
        print("❌ Validation error:")
        print(e)
        raise

    print("✅ MODELS validated successfully!")
    
    # Create LangChain agents
    try:
        modelos = validated.create_agents()
        print("\n✅ Agents created successfully!")
        print(f"models = {{")
        for name, agent in modelos.items():
            model_config = next(m for m in validated.models if m.name == name)
            agent_type = type(agent).__name__
            print(f"    '{name}': {agent_type}(")
            print(f"        model=\"{model_config.model}\",")
            print(f"        temperature={model_config.temperature},")
            print(f"        max_tokens={model_config.max_tokens},")
            if "gemini" in name.lower():
                print(f"        google_api_key=\"{model_config.key[:10]}...\"")
            elif "anthropic" in name.lower() or "claude" in name.lower():
                print(f"        api_key=\"{model_config.key[:10]}...\"")
            else:
                print(f"        api_key=\"{model_config.key[:10]}...\"")
            print(f"    ),")
        print(f"}}")
    except (ImportError, ValueError) as e:
        print(f"\n⚠️  Error: Could not create agents: {e}")
        print("\nTo install required packages (LangChain 1.0):")
        print("  pip install langchain-google-genai  # For Gemini models")
        print("  pip install langchain-openai        # For OpenAI/GPT models")
        print("  pip install langchain-anthropic     # For Anthropic/Claude models")
