from typing import List, Literal
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from app.services.llm.llm_factory import LLMFactory
from app.services.llm.llm_setting import LLMConfig
from app.utils.logger_service import LoggerService

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
       - "EmailAgent" → Send to email agent
       - "Researcher" → Send to researcher agent
       - "SqlAgent" → Send to SQL agent
       - "FINISH" → End the workflow
    """
    next: Literal["FINISH", "EmailAgent", "Researcher", "SqlAgent"]


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
    def __init__(self, provider=None, model_name=None):
        """
        Initialize the supervisor agent.
        
        Args:
            model_name: The LLM model to use
        """
        self.logger = LoggerService.get_instance().get_logger(__name__)
        self.members = ["EmailAgent", "Researcher", "SqlAgent"]
        self.options = ["FINISH"] + self.members
        provider = provider or LLMConfig.PROVIDER
        model_name = model_name or LLMConfig.MODEL_NAME
        
        system_prompt = (
            "You are a supervisor tasked with managing a conversation between the" 
            " following workers (agents): {members}. Given the following user request,"
            " respond with the worker to act next. Each worker will perform a task and respond with their results and status."
            "Worker (agents) specialties:"
            "\n1. EmailAgent: For sending emails to users with course information."
            "  1.1 When the user asks to SEND AN EMAIL to a user (Example: Semd an email to Jon with his completed courses)."            
            "\n2. Researcher: For general information gathering, online research, web research, and non-database questions"
            "  2.1 Exemple: When the user asks about general information, research topics, or any data that would require web search."
            "\n3. SqlAgent: For database queries, SQL operations, and data retrieval from the Course Management system"
            "\ 3.1 Exemple: When the user asks about database information, users, courses, roles, or any data that would require SQL queries."
            "\n4. When finished, respond with FINISH."
        )
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "user",
                    "Given the conversation above, who should act next?" 
                    " Or should we FINISH? Select one of: {options}"
                ),
            ]
        ).partial(options=str(self.options), members=", ".join(self.members))
        
        self.llm = LLMFactory.get_instance().get_llm(provider, model_name)

    
    
    #--------------------------------------------------------------------------------
    # Define the __call__ method to process the current state and decide on the next routing step
    #--------------------------------------------------------------------------------    
    def __call__(self, state):
        try:
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
        
        except Exception as e:
            self.logger.error(f"Error processing supervisor routing decision: {str(e)}")
            raise Exception("Supervisor routing error.")