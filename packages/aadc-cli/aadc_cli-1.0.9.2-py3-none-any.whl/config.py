"""
Configuration module for AADC
Handles API keys and settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from current directory first, then home directory
# This allows project-specific .env to override global settings
load_dotenv()  # Load from current directory
load_dotenv(Path.home() / ".aadc" / ".env")  # Load from home directory

# Available models and their providers
AVAILABLE_MODELS = {
    "auto": {
        "provider": "auto",
        "display_name": "Auto (Smart Routing)",
        "router_model": "nova-2-lite",
        "simple_model": "nova-2-lite",
        "complex_model": "gemini-3-pro-preview"
    },
    "gemini-3-pro-preview": {
        "provider": "gemini",
        "display_name": "Gemini 3 Pro Preview",
        "api_key_env": "GEMINI_API_KEY",
        "openrouter_id": "google/gemini-pro-1.5"  # OpenRouter equivalent
    },
    "gemini-2.5-pro": {
        "provider": "gemini", 
        "display_name": "Gemini 2.5 Pro",
        "api_key_env": "GEMINI_API_KEY",
        "openrouter_id": "google/gemini-pro-1.5"
    },
    "gemini-2.5-flash": {
        "provider": "gemini", 
        "display_name": "Gemini 2.5 Flash",
        "api_key_env": "GEMINI_API_KEY",
        "openrouter_id": "google/gemini-flash-1.5"
    },
    "gpt-5.1": {
        "provider": "openai",
        "display_name": "GPT-5.1",
        "api_key_env": "OPENAI_API_KEY",
        "openrouter_id": "openai/gpt-5.1",
        "coming_soon": True
    },
    "GPT-5.1-Codex": {
        "provider": "openai",
        "display_name": "GPT-5.1 Codex", 
        "api_key_env": "OPENAI_API_KEY",
        "openrouter_id": "openai/GPT-5.1-Codex",
        "coming_soon": True
    },
    "GPT-5.1-Codex-Mini": {
        "provider": "openai",
        "display_name": "GPT-5.1 Codex Mini", 
        "api_key_env": "OPENAI_API_KEY",
        "openrouter_id": "openai/GPT-5.1-Codex-Mini",
        "coming_soon": True
    },
    "anthropic/claude-opus-4.5": {
        "provider": "anthropic",
        "display_name": "Claude Opus 4.5",
        "api_key_env": "ANTHROPIC_API_KEY",
        "openrouter_id": "anthropic/claude-opus-4.5",
        "coming_soon": True
    },
    "anthropic/claude-sonnet-4.5": {
        "provider": "anthropic",
        "display_name": "Claude Sonnet 4.5",
        "api_key_env": "ANTHROPIC_API_KEY",
        "openrouter_id": "anthropic/claude-sonnet-4.5",
        "coming_soon": True
    },
    "anthropic/claude-haiku-4.5": {
        "provider": "anthropic",
        "display_name": "Claude Haiku 4.5",
        "api_key_env": "ANTHROPIC_API_KEY",
        "openrouter_id": "anthropic/claude-haiku-4.5",
        "coming_soon": True
    },
    "nova-2-lite": {
        "provider": "openrouter",
        "display_name": "Nova 2 Lite",
        "api_key_env": "OPENROUTER_API_KEY",
        "openrouter_id": "amazon/nova-2-lite-v1:free"
    }
}

# OpenRouter model ID mapping for using models via OpenRouter
OPENROUTER_MODEL_MAP = {
    "gemini": "google/gemini-pro-1.5",
    "openai": "openai/gpt-4o", 
    "anthropic": "anthropic/claude-3.5-sonnet"
}

# Default configuration
DEFAULT_CONFIG = {
    "model": "auto",  # Model to use (default to auto routing)
    "max_tokens": 65536,  # Maximum response tokens
    "temperature": 0.7,  # Creativity level
    "timeout": 300,  # API timeout in seconds
    "max_iterations": 50,  # Maximum tool call iterations per request
    "confirm_destructive": False,  # Ask before delete operations
    "working_directory": os.getcwd(),  # Default working directory
    "permission_mode": "auto",  # Permission mode: "ask", "auto", "command_ask"
    "plan_mode": False,  # Whether to create plan.md before coding
    "use_openrouter": False,  # Whether to route through OpenRouter API
}


# Permission mode descriptions
PERMISSION_MODES = {
    "ask": "Ask before executing ANY tool",
    "auto": "Execute all tools automatically (no confirmations)",
    "command_ask": "Only ask before executing shell commands"
}


def get_api_key(key_name: str = "GEMINI_API_KEY") -> str:
    """
    Get an API key from environment variable (loaded from .env or exported).
    """
    return os.environ.get(key_name, "")


def get_model_api_key(model_name: str) -> str:
    """Get the appropriate API key for a model."""
    if model_name in AVAILABLE_MODELS:
        key_env = AVAILABLE_MODELS[model_name]["api_key_env"]
        return get_api_key(key_env)
    return ""


def save_api_key(api_key: str, key_name: str = "GEMINI_API_KEY") -> None:
    """
    Save API key to user's home directory for future use.
    """
    config_dir = Path.home() / ".aadc"
    config_dir.mkdir(exist_ok=True)
    
    env_file = config_dir / ".env"
    
    # Read existing content
    existing = {}
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    existing[k] = v
    
    # Update with new key
    existing[key_name] = api_key
    
    # Write back
    with open(env_file, 'w') as f:
        for k, v in existing.items():
            f.write(f"{k}={v}\n")
    
    # Set restrictive permissions
    env_file.chmod(0o600)


class Config:
    """Configuration manager for the agent."""
    
    def __init__(self):
        self._config = DEFAULT_CONFIG.copy()
        self._api_keys = {}
    
    def get_api_key(self, model_name: str = None) -> str:
        """Get API key for current or specified model."""
        model = model_name or self._config["model"]
        if model in AVAILABLE_MODELS:
            key_env = AVAILABLE_MODELS[model]["api_key_env"]
            if key_env not in self._api_keys:
                self._api_keys[key_env] = get_api_key(key_env)
            return self._api_keys[key_env]
        return ""
    
    def set_api_key(self, key: str, key_name: str = None):
        """Set an API key."""
        if key_name is None:
            model = self._config["model"]
            if model in AVAILABLE_MODELS:
                key_name = AVAILABLE_MODELS[model]["api_key_env"]
            else:
                key_name = "GEMINI_API_KEY"
        self._api_keys[key_name] = key
        os.environ[key_name] = key
    
    @property
    def api_key(self) -> str:
        return self.get_api_key()
    
    @api_key.setter
    def api_key(self, value: str):
        self.set_api_key(value)
    
    @property
    def model(self) -> str:
        return self._config["model"]
    
    @model.setter
    def model(self, value: str):
        if value in AVAILABLE_MODELS:
            self._config["model"] = value
    
    @property
    def model_provider(self) -> str:
        """Get the provider for current model."""
        model = self._config["model"]
        if model in AVAILABLE_MODELS:
            return AVAILABLE_MODELS[model]["provider"]
        return "gemini"
    
    @property
    def max_tokens(self) -> int:
        return self._config["max_tokens"]
    
    @property
    def temperature(self) -> float:
        return self._config["temperature"]
    
    @property
    def timeout(self) -> int:
        return self._config["timeout"]
    
    @property
    def max_iterations(self) -> int:
        return self._config["max_iterations"]
    
    @property
    def confirm_destructive(self) -> bool:
        return self._config["confirm_destructive"]
    
    @property
    def working_directory(self) -> str:
        return self._config["working_directory"]
    
    @working_directory.setter
    def working_directory(self, value: str):
        self._config["working_directory"] = value
    
    @property
    def permission_mode(self) -> str:
        return self._config["permission_mode"]
    
    @permission_mode.setter
    def permission_mode(self, value: str):
        if value in PERMISSION_MODES:
            self._config["permission_mode"] = value
    
    @property
    def plan_mode(self) -> bool:
        return self._config["plan_mode"]
    
    @plan_mode.setter
    def plan_mode(self, value: bool):
        self._config["plan_mode"] = value
    
    @property
    def use_openrouter(self) -> bool:
        return self._config["use_openrouter"]
    
    @use_openrouter.setter
    def use_openrouter(self, value: bool):
        self._config["use_openrouter"] = value
    
    @property
    def github_auto_commit(self) -> bool:
        """Enable/disable automatic GitHub commits after file edits."""
        return self._config.get("github_auto_commit", False)
    
    @github_auto_commit.setter
    def github_auto_commit(self, value: bool):
        self._config["github_auto_commit"] = value
    
    def update(self, **kwargs):
        """Update configuration values."""
        for key, value in kwargs.items():
            if key in self._config:
                self._config[key] = value


# Global config instance
config = Config()
