"""
LLM configuration management.

Handles loading API keys and configuration from llm.yml file.
"""

from pathlib import Path
from typing import Dict, Optional, Any
import yaml
import os


def load_llm_config() -> Dict[str, Any]:
    """
    Load LLM configuration from llm.yml file.
    
    Returns:
        Dictionary containing configuration including API keys and base URLs
    """
    config_file = Path("llm.yml")
    
    if not config_file.exists():
        # Try alternative locations
        config_file = Path.cwd() / "llm.yml"
        if not config_file.exists():
            config_file = Path.home() / ".brainary" / "llm.yml"
    
    if not config_file.exists():
        return {}
    
    with config_file.open("r") as f:
        config = yaml.safe_load(f) or {}
    return config


def get_openai_config() -> tuple[Optional[str], Optional[str]]:
    """
    Get OpenAI API configuration.
    
    Returns:
        Tuple of (api_key, base_url)
    """
    config = load_llm_config()
    
    # Try config file first, then environment variables
    api_key = config.get("openai-key") or os.getenv("OPENAI_API_KEY")
    base_url = config.get("openai-base-url") or os.getenv("OPENAI_BASE_URL")
    
    return api_key, base_url


def get_anthropic_config() -> Optional[str]:
    """
    Get Anthropic API configuration.
    
    Returns:
        API key
    """
    config = load_llm_config()
    
    # Try config file first, then environment variable
    api_key = config.get("anthropic-key") or os.getenv("ANTHROPIC_API_KEY")
    
    return api_key


def get_ollama_config() -> Optional[str]:
    """
    Get Ollama configuration.
    
    Returns:
        Base URL for Ollama server
    """
    config = load_llm_config()
    
    # Default to localhost if not specified
    base_url = config.get("ollama-base-url") or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    return base_url
