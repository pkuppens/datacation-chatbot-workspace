"""Configuration management for the chatbot workshop project."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ConfigurationError(Exception):
    """Base exception for configuration errors."""

    pass


class MissingAPIKeyError(ConfigurationError):
    """Raised when a required API key is missing."""

    pass


@dataclass
class ModelConfig:
    """Configuration for language models."""

    name: str
    temperature: float
    max_tokens: int
    top_p: float
    top_k: int

    @classmethod
    def from_env(cls) -> "ModelConfig":
        """Create ModelConfig from environment variables."""
        return cls(
            name=os.getenv("MODEL_NAME", "gemini-pro"),
            temperature=float(os.getenv("MODEL_TEMPERATURE", "0.3")),
            max_tokens=int(os.getenv("MODEL_MAX_TOKENS", "8192")),
            top_p=float(os.getenv("MODEL_TOP_P", "0.8")),
            top_k=int(os.getenv("MODEL_TOP_K", "20")),
        )

    def validate(self) -> None:
        """Validate model configuration values.

        Raises:
            ConfigurationError: If validation fails
        """
        if not 0 <= self.temperature <= 1:
            raise ConfigurationError(f"Temperature must be between 0 and 1, got {self.temperature}")

        if self.max_tokens < 1:
            raise ConfigurationError(f"Max tokens must be positive, got {self.max_tokens}")

        if not 0 < self.top_p <= 1:
            raise ConfigurationError(f"Top-p must be between 0 and 1, got {self.top_p}")

        if self.top_k < 1:
            raise ConfigurationError(f"Top-k must be positive, got {self.top_k}")


@dataclass
class DataPipelineConfig:
    """Configuration for data pipelines."""

    cache_expiration: int = 3600  # 1 hour
    data_sources_dir: Path = Path("data_sources")
    titanic_db_name: str = "titanic.db"


@dataclass
class VectorStoreConfig:
    """Configuration for vector stores."""

    enabled: bool = False
    type: str = "chroma"  # or "faiss", "pinecone", etc.
    persist_directory: Path = Path("vector_store")


@dataclass
class MemoryConfig:
    """Configuration for conversation memory."""

    enabled: bool = True
    type: str = "buffer"  # or "summary", "vector", etc.
    max_tokens: int = 2000


@dataclass
class AppConfig:
    """Configuration for the application."""

    debug: bool = False
    log_level: str = "INFO"
    port: int = 8000
    host: str = "localhost"


class Config:
    """Main configuration class."""

    def __init__(self):
        self.model = ModelConfig.from_env()
        self.pipeline = DataPipelineConfig()
        self.vector_store = VectorStoreConfig()
        self.memory = MemoryConfig()
        self.app = AppConfig()

    def get_api_key(self, key_name: str) -> str:
        """Get an API key with validation.

        Args:
            key_name: Name of the API key to retrieve

        Returns:
            The API key value

        Raises:
            MissingAPIKeyError: If the key is missing or empty
        """
        key = os.getenv(key_name)
        if not key:
            raise MissingAPIKeyError(f"Required API key '{key_name}' is missing or empty")
        return key

    @property
    def google_api_key(self) -> str:
        """Get the Google API key."""
        return self.get_api_key("GOOGLE_API_KEY")

    @property
    def openai_api_key(self) -> Optional[str]:
        """Get the OpenAI API key if available."""
        return os.getenv("OPENAI_API_KEY")

    @property
    def huggingface_api_key(self) -> Optional[str]:
        """Get the HuggingFace API key if available."""
        return os.getenv("HUGGINGFACE_API_KEY")

    def validate(self) -> None:
        """Validate the configuration.

        Raises:
            ConfigurationError: If validation fails
        """
        # Validate model configuration
        self.model.validate()

        # Ensure required directories exist
        self.pipeline.data_sources_dir.mkdir(parents=True, exist_ok=True)
        if self.vector_store.enabled:
            self.vector_store.persist_directory.mkdir(parents=True, exist_ok=True)

        # Validate log level
        valid_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.app.log_level not in valid_log_levels:
            raise ConfigurationError(f"Invalid log level: {self.app.log_level}")

        # Validate port number
        if not 0 < self.app.port < 65536:
            raise ConfigurationError(f"Invalid port number: {self.app.port}")


# Create global config instance
config = Config()

# Validate configuration on import
config.validate()
