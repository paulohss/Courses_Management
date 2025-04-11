import functools
from langgraph.graph import END, StateGraph, START
from app.services.agent.factory.agent_state import AgentState
from app.services.agent.factory.helpers import agent_node
from app.services.agent.sql_agent import SqlAgent
from app.services.agent.supervisor_agent import SupervisorAgent
from app.services.agent.researcher_agent import ResearcherAgent
from app.services.agent.email_agent import EmailAgent
from app.services.llm.llm_setting import LLMConfig
from app.utils.logger_service import LoggerService


class MultiAgentWorkflow:
    """
    Creates and manages a workflow graph connecting multiple agents.
    """
    
    #--------------------------------------------------------------------------------
    # Define the __init__ method to initialize the multi-agent workflow
    #--------------------------------------------------------------------------------
    def __init__(self, provider=None, model_name=None):
        self.logger = LoggerService.get_instance().get_logger(__name__)
        
        # Use config if not provided
        provider = provider or LLMConfig.PROVIDER
        model_name = model_name or LLMConfig.MODEL_NAME
        
        self.logger.info(f"Initializing MultiAgentWorkflow with provider: {provider}, model: {model_name}")
        
        # Create agents with specified provider and model
        self.supervisor_agent = SupervisorAgent(provider, model_name)
        self.researcher_agent = ResearcherAgent(provider, model_name)
        self.sql_agent = SqlAgent(provider, model_name)
        self.email_agent = EmailAgent(provider, model_name)
        
        self.members = ["Researcher", "SqlAgent", "EmailAgent"]
        self.graph = None  # Will be initialized when build_graph() is called
    
    
    #--------------------------------------------------------------------------------
    # Define the build_graph method to build the workflow graph connecting the agents
    #--------------------------------------------------------------------------------
    def build_graph(self):
        try:
            """
            Build the workflow graph connecting the agents.
            
            Returns:
                The compiled workflow graph
            """
            workflow = StateGraph(AgentState)
            
            # Add nodes for each agent, starting with Supervisor
            workflow.add_node("supervisor", self.supervisor_agent)
            
            # Add email agent
            workflow.add_node("EmailAgent", functools.partial(
                agent_node, agent=self.email_agent, name="EmailAgent")
            )
            
            # Researcher Agent (researcher_agent.agent)
            research_node = functools.partial(
                agent_node, agent=self.researcher_agent.agent, name="Researcher"
            )
            workflow.add_node("Researcher", research_node)
            
            # SQL Agent - Add SqlAgent Class directly (self.sql_agent) so the proper Invoke method is called
            sql_node = functools.partial(
                agent_node, agent=self.sql_agent, name="SqlAgent"
            )
            workflow.add_node("SqlAgent", sql_node)        
            
            # Add Graph Edges
            for member in self.members:
                # Workers always report back to the supervisor
                workflow.add_edge(member, "supervisor")
            
            # The supervisor populates the NEXT field in the graph state
            # which routes to a node or finishes
            conditional_map = {k: k for k in self.members}
            conditional_map["FINISH"] = END
            workflow.add_conditional_edges(
                "supervisor", lambda x: x["next"], conditional_map
            )
            
            # Add entry point
            workflow.add_edge(START, "supervisor")
            
            self.graph = workflow.compile()
            return self.graph
        
        except Exception as e:
            self.logger.error(f"Error building workflow graph: {str(e)}")
    
    
    
    """
    The functools.partial() creates a new function where:
    - It's based on the agent_node helper function
    - The 'agent' and 'name' parameters are permanently set
    - Only the 'state' parameter will need to be provided when this function is called
    - This makes the node reusable without repeating these arguments
    """