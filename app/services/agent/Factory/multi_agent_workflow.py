import functools
from langgraph.graph import END, StateGraph, START
from app.services.agent.factory.agent_state import AgentState
from app.services.agent.factory.agents_util import AgentsUtil
from app.services.agent.factory.helpers import agent_node
from app.services.agent.sql_agent import SqlAgent
from app.services.agent.supervisor_agent import SupervisorAgent
from app.services.agent.researcher_agent import ResearcherAgent
from app.services.agent.email_agent import EmailAgent
from app.services.agent.rag_pdf import RagPdfAgent
from app.services.agent.chart_agent import ChartAgent  
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
        self.rag_pdf_agent = RagPdfAgent(provider, model_name)
        self.chart_agent = ChartAgent(provider, model_name)  
        
        self.members = AgentsUtil.get_members()
        self.graph = None 
    
    
    #--------------------------------------------------------------------------------
    # Define the build_graph method to build the workflow graph connecting the agents
    #--------------------------------------------------------------------------------
    def build_graph(self):
        try:
            workflow = StateGraph(AgentState)
            
            # Add nodes for each agent, starting with Supervisor
            workflow.add_node("supervisor", self.supervisor_agent)            
                                    
            # Researcher Agent --------------------------------------------------
            research_node = functools.partial(
                agent_node, agent=self.researcher_agent.agent, name="Researcher"
            )
            workflow.add_node("Researcher", research_node)
            # --------------------------------------------------------------------
            
            # SQL Agent ----------------------------------------------------------            
            sql_node = functools.partial(
                agent_node, agent=self.sql_agent, name="SqlAgent" # Add directly (self.sql_agent) so the Invoke method is called
            )
            workflow.add_node("SqlAgent", sql_node)        
            #--------------------------------------------------------------------

            # Add email agent ---------------------------------------------------
            email_node = functools.partial(
                agent_node, agent=self.email_agent, name="EmailAgent"
            )
            workflow.add_node("EmailAgent", email_node)
            # --------------------------------------------------------------------
            
            # Rag PDF agent-------------------------------------------------------
            rag_pdf_node = functools.partial(
                agent_node, agent=self.rag_pdf_agent, name="RagPdfAgent"
            )
            workflow.add_node("RagPdfAgent", rag_pdf_node)        
            # --------------------------------------------------------------------
            
            # Chart Agent --------------------------------------------------------
            chart_node = functools.partial(
                agent_node, agent=self.chart_agent, name="ChartAgent"
            )
            workflow.add_node("ChartAgent", chart_node)
            # --------------------------------------------------------------------
            
            # Add Graph Edges
            for member in self.members:
                # Workers always report back to the supervisor
                workflow.add_edge(member, "supervisor")              
            
            # The supervisor populates the NEXT field in the graph state which routes to a node or finishes
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
    
    
    
