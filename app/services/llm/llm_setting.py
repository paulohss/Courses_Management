class LLMConfig:
    # Default provider settings
    PROVIDER = "openai"  # Options: "openai", "ollama"
    MODEL_NAME = "gpt-4o" # "gpt-3.5-turbo", "gpt-4", "gpt-4o", "llama3.2"
    
    # Provider-specific settings
    OPENAI_API_KEY = None  # Will use environment variable if None
    OLLAMA_BASE_URL = "http://localhost:11434"