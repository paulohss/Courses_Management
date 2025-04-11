from langchain_openai import ChatOpenAI
from app.services.llm.llm_factory import LLMFactory
from app.services.llm.llm_setting import LLMConfig
from app.utils.logger_service import LoggerService
from app.services.agent.prompt.supervisor_route_response import RouteResponse




#--------------------------------------------------------------------------------
# Define the SupervisorAgent class to coordinate the work between researcher and coder agents
#--------------------------------------------------------------------------------
class SupervisorAgent:
    
    #--------------------------------------------------------------------------------
    # Define the __init__ method to initialize the supervisor agent
    #--------------------------------------------------------------------------------
    def __init__(self, provider=None, model_name=None):

        self.logger = LoggerService.get_instance().get_logger(__name__)
        self.members = ["EmailAgent", "Researcher", "SqlAgent"]
        self.options = ["FINISH"] + self.members
        provider = provider or LLMConfig.PROVIDER
        model_name = model_name or LLMConfig.MODEL_NAME
                
        self.prompt = RouteResponse.get_route_prompt(self.options, self.members)
        
        self.llm = LLMFactory.get_instance().get_llm(provider, model_name)



    
    
    #--------------------------------------------------------------------------------
    # Define the __call__ method to process the current state and decide on the next routing step
    #--------------------------------------------------------------------------------    
    def __call__(self, state):
        try:
            email_terms = ["send an email", "send email", "email the", "send to"]
            
            # Check the latest message in the state for email-related terms
            if state["messages"]:
                latest_message = state["messages"][-1]  # Get the latest message
                if any(term in latest_message.content.lower() for term in email_terms):
                    return RouteResponse(next="EmailAgent")
                
            
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