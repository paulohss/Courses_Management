from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

class ResearcherAgent:
    """
    Agent responsible for performing research tasks using Tavily search.
    """
    #-------------------------------------------------------------------------------- 
    # Define the __init__ method to initialize the researcher agent
    #--------------------------------------------------------------------------------
    def __init__(self, model_name="gpt-4o"):
        """
        Initialize the researcher agent.
        
        Args:
            model_name: The LLM model to use
        """
        self.llm = ChatOpenAI(model=model_name)
        self.tavily_tool = TavilySearchResults(max_result=5)
        self.agent = create_react_agent(self.llm, tools=[self.tavily_tool])
    
