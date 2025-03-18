from abc import ABC, abstractmethod
from app.utils.logger_service import LoggerService

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self):
        self.logger = LoggerService.get_instance().get_logger(__name__)
    
    @abstractmethod
    def get_llm(self, model_name: str):
        """Returns a configured LLM instance"""
        pass
    
    @abstractmethod
    def get_available_models(self) -> list:
        """Returns a list of available models for this provider"""
        pass