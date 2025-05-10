# Environment Configuration

## Overview

This project uses environment variables for configuration management. This approach:

- Keeps sensitive information secure
- Makes configuration flexible across different environments
- Follows the twelve-factor app methodology
- Makes it easy to change settings without code modifications

## Setup

1. Copy the example environment file:

   ```bash
   cp env.example .env
   ```

2. Edit `.env` and fill in your actual values:
   - Required secrets (API keys)
   - Optional configuration settings
   - Environment-specific values

3. Never commit the `.env` file to version control
   - It's already in `.gitignore`
   - Contains sensitive information
   - Should be managed securely

## Configuration Categories

### 1. API Keys and Secrets

These are sensitive credentials that must be kept secure:

- `GOOGLE_API_KEY`: Required for Gemini/Vertex AI access
- `OPENAI_API_KEY`: Optional, for OpenAI model access
- `HUGGINGFACE_API_KEY`: Optional, for HuggingFace model access

### 2. Model Configuration

Settings that control the behavior of language models:

- `MODEL_NAME`: The specific model to use (e.g., gemini-pro)
- `MODEL_TEMPERATURE`: Controls response randomness (0.0-1.0)
- `MODEL_MAX_TOKENS`: Maximum length of model responses
- `MODEL_TOP_P`: Nucleus sampling parameter
- `MODEL_TOP_K`: Top-k sampling parameter

### 3. Data Pipeline Settings

Configuration for the Prefect-based data pipeline:

- `DATA_CACHE_EXPIRATION`: How long to cache data (seconds)
- `DATA_SOURCES_DIR`: Where to store datasets
- `TITANIC_DB_NAME`: Name of the SQLite database

### 4. Application Settings

General application configuration:

- `DEBUG`: Enable debug mode
- `LOG_LEVEL`: Control logging verbosity
- `PORT`: Web interface port
- `HOST`: Web interface host

### 5. Database Settings

Configuration for database connections:

- `DB_HOST`: Database server host
- `DB_PORT`: Database server port
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password

### 6. Feature Flags

Toggle specific features:

- `ENABLE_VECTOR_STORE`: Enable vector storage
- `ENABLE_MEMORY`: Enable conversation memory
- `ENABLE_STREAMING`: Enable streaming responses

### 7. Cache Settings

Configuration for caching:

- `CACHE_TYPE`: Type of cache to use
- `CACHE_TTL`: Cache time-to-live

## Best Practices

1. **Security**
   - Never commit `.env` to version control
   - Use strong, unique values for secrets
   - Rotate API keys regularly
   - Use environment-specific values

2. **Development**
   - Use `.env.example` as a template
   - Document all new environment variables
   - Provide sensible defaults where possible
   - Keep secrets empty in example file

3. **Deployment**
   - Set up environment variables in deployment platform
   - Use secure secret management
   - Validate configuration on startup
   - Log configuration issues clearly

## Usage in Code

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Access configuration
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("MODEL_NAME", "gemini-pro")  # With default
debug = os.getenv("DEBUG", "false").lower() == "true"
```

## Troubleshooting

Common issues and solutions:

1. **Missing Environment Variables**
   - Check if `.env` exists
   - Verify variable names
   - Ensure proper loading

2. **Invalid Values**
   - Check value formats
   - Verify ranges
   - Look for typos

3. **Security Issues**
   - Rotate compromised keys
   - Check file permissions
   - Verify `.gitignore`

## Adding New Configuration

When adding new environment variables:

1. Add to `.env.example` with:
   - Clear description
   - Default value if appropriate
   - Empty value for secrets

2. Update this documentation

3. Add validation in code

4. Test in different environments
