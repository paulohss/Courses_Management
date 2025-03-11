from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

class CoderAgent:
    """
    Agent responsible for executing code and providing coding solutions.
    CAUTION: Uses PythonREPLTool which executes arbitrary code.
    """
    
    #--------------------------------------------------------------------------------
    # Define the __init__ method to initialize the coder 
    #--------------------------------------------------------------------------------
    def __init__(self, model_name="gpt-4o"):
        """
        Initialize the coder agent.
        
        Args:
            model_name: The LLM model to use
        """
        self.llm = ChatOpenAI(model=model_name)
        self.python_repl_tool = PythonREPLTool()
        self.agent = create_react_agent(self.llm, tools=[self.python_repl_tool])
    
    
    #--------------------------------------------------------------------------------
    # Define the invoke method to process the current state and perform coding tasks
    #--------------------------------------------------------------------------------    
    def invoke(self, state):
        """
        Process the current state and perform coding tasks.
        
        Args:
            state: Current state with messages
            
        Returns:
            Result of the agent's processing
        """
        return self.agent.invoke(state)