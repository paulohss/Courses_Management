from app.services.llm.llm_implementation import OpenAIProvider, OllamaProvider
from app.utils.logger_service import LoggerService

class LLMFactory:
    """Factory for creating LLM instances based on configuration"""
    _instance = None
    
    # ----------------------------------------------------------------------------------------
    # Get Instance
    # ----------------------------------------------------------------------------------------
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = LLMFactory()
        return cls._instance
    
    # ----------------------------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------------------------
    def __init__(self):
        self.logger = LoggerService.get_instance().get_logger(__name__)
        self.providers = {
            "openai": OpenAIProvider(),
            "ollama": OllamaProvider()
        }
        self.default_provider = "openai"
        self.default_models = {
            "openai": "gpt-4o",
            "ollama": "llama3.2"
        }
    
    
    # ----------------------------------------------------------------------------------------
    # Get LLM
    # ----------------------------------------------------------------------------------------
    def get_llm(self, provider_name=None, model_name=None):
        """Get an LLM instance based on provider and model name"""
        try:
            provider_name = provider_name or self.default_provider
            
            if provider_name not in self.providers:
                self.logger.warning(f"Provider {provider_name} not found. Using {self.default_provider}.")
                provider_name = self.default_provider
            
            provider = self.providers[provider_name]
            model_name = model_name or self.default_models[provider_name]
            
            return provider.get_llm(model_name)
            
        except Exception as e:
            self.logger.error(f"Error creating LLM: {str(e)}")
            return self.providers["openai"].get_llm("gpt-4o")