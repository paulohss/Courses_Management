from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from app.services.llm.llm_provider import LLMProvider


# -----------------------------------------------------------------------------------------------------------------------------------
# LLMProvider Implementations - OpenAIProvider
# -----------------------------------------------------------------------------------------------------------------------------------
class OpenAIProvider(LLMProvider):
    def __init__(self, api_key=None):
        super().__init__()
        self.api_key = api_key
    
    def get_llm(self, model_name="gpt-4o"):
        self.logger.info(f"Creating OpenAI LLM with model: {model_name}")
        return ChatOpenAI(model=model_name, api_key=self.api_key)
    
    def get_available_models(self):
        return ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]



# -----------------------------------------------------------------------------------------------------------------------------------
# LLMProvider Implementations - OllamaProvider
# -----------------------------------------------------------------------------------------------------------------------------------
class OllamaProvider(LLMProvider):
    def __init__(self, base_url="http://localhost:11434"):
        super().__init__()
        self.base_url = base_url
    
    def get_llm(self, model_name="llama3.2"):
        self.logger.info(f"Creating Ollama LLM with model: {model_name}")
        return Ollama(model=model_name, base_url=self.base_url)
    
    def get_available_models(self):
        return ["llama3.2", "deepseek-r1:14b"]
