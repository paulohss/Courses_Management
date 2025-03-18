from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from app.services.llm.llm_factory import LLMFactory
from app.services.llm.llm_setting import LLMConfig

class ResearcherAgent:
    """
    Agent responsible for performing research tasks using Tavily search.
    """
    #-------------------------------------------------------------------------------- 
    # Define the __init__ method to initialize the researcher agent
    #--------------------------------------------------------------------------------
    def __init__(self, provider=None, model_name=None):
        """
        Initialize the researcher agent.
        
        Args:
            provider: The LLM provider to use (default from config)
            model_name: The specific model to use (default from config)
        """
        # Get LLM from factory
        provider = provider or LLMConfig.PROVIDER
        model_name = model_name or LLMConfig.MODEL_NAME
        
        self.llm = LLMFactory.get_instance().get_llm(provider, model_name)
        self.tavily_tool = TavilySearchResults(max_result=5)
        self.agent = create_react_agent(self.llm, tools=[self.tavily_tool])
    
