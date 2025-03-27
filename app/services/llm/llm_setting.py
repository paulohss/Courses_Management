class LLMConfig:
    # Default provider settings
    PROVIDER = "ollama"  # Options: "openai", "ollama"
    MODEL_NAME = "llama3.1:8b-instruct-q4_0" # "gpt-3.5-turbo", "gpt-4", "gpt-4o", "llama3.2"
    
    # Provider-specific settings
    OPENAI_API_KEY = None  # Will use environment variable if None
    OLLAMA_BASE_URL = "http://localhost:11434"