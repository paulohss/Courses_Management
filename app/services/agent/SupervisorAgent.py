from typing import List, Literal
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# Define the allowed routing decisions for the supervisor agent
class RouteResponse(BaseModel):
    """
    Response model for supervisor routing decisions.
    
    This class defines a structured output format using Pydantic:
    
    1. Creates a schema that enforces what values the supervisor can return
       when deciding the next step in the workflow.
    
    2. By inheriting from Pydantic's BaseModel, it gains automatic data
       validation, serialization, and documentation capabilities.
    
    3. The 'next' field uses Python's Literal type to restrict valid values to only
       three specific options: "FINISH", "Researcher", or "SqlAgent". Any other value
       would cause a validation error.
    
    4. Used with .with_structured_output(RouteResponse) to instruct the LLM to
       format its response according to this schema, ensuring the supervisor agent
       always returns one of the three valid routing options.
    
    5. Controls workflow routing:
       - "Researcher" → Send to researcher agent
       - "SqlAgent" → Send to SQL agent
       - "FINISH" → End the workflow
    """
    next: Literal["FINISH", "Researcher", "SqlAgent"]


#--------------------------------------------------------------------------------
# Define the SupervisorAgent class to coordinate the work between researcher and coder agents
#--------------------------------------------------------------------------------
class SupervisorAgent:
    """
    Agent responsible for coordinating the work between researcher and coder agents.
    Decides which agent should work next or if the task is complete.
    """
    
    #--------------------------------------------------------------------------------
    # Define the __init__ method to initialize the supervisor agent
    #--------------------------------------------------------------------------------
    def __init__(self, model_name="gpt-4o"):
        """
        Initialize the supervisor agent.
        
        Args:
            model_name: The LLM model to use
        """
        self.members = ["Researcher", "SqlAgent"]
        self.options = ["FINISH"] + self.members
        
        system_prompt = (
            "You are a supervisor tasked with managing a conversation between the" 
            " following workers: {members}. Given the following user request,"
            " respond with the worker to act next. Each worker will perform a"
            " task and respond with their results and status."
            "\n\nWorker specialties:"
            "\n- Researcher: For general information gathering, web research, and non-database questions"
            "\n- SqlAgent: For database queries, SQL operations, and data retrieval from the Course Management system"
            "\n\nWhen the user asks about database information, users, courses, roles, or any data that would"
            " require SQL queries, always route to SqlAgent first."
            "\n\nWhen finished, respond with FINISH."
        )
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "system",
                    "Given the conversation above, who should act next?" 
                    " Or should we FINISH? Select one of: {options}"
                ),
            ]
        ).partial(options=str(self.options), members=", ".join(self.members))
        
        self.llm = ChatOpenAI(model=model_name)
    
    
    #--------------------------------------------------------------------------------
    # Define the __call__ method to process the current state and decide on the next routing step
    #--------------------------------------------------------------------------------    
    def __call__(self, state):
        """
        Process the current state and decide on the next routing step.
        
        Args:
            state: Current state with messages
            
        Returns:
            Dict containing the next routing step
        """
        # Step 1: Configure the LLM to output structured data according to our model
        structured_llm = self.llm.with_structured_output(RouteResponse)
        
        # Step 2: Create a decision chain by combining our prompt template with the structured LLM
        routing_chain = self.prompt | structured_llm
        
        # Step 3: Process the current state through the chain to determine next step
        routing_decision = routing_chain.invoke(state)
        
        return routing_decision