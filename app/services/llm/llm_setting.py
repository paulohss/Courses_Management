class LLMConfig:
    # Default provider settings
    PROVIDER = "openai"  # Options: "openai", "ollama"
    MODEL_NAME = "gpt-4o" # Default model for the selected provider
    
    # Provider-specific settings
    OPENAI_API_KEY = None  # Will use environment variable if None
    OLLAMA_BASE_URL = "http://localhost:11434"