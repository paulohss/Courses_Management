import functools
from langgraph.graph import END, StateGraph, START
from app.services.agent.Factory.AgentState import AgentState
from app.services.agent.Factory.Helpers import agent_node
from app.services.agent.SqlAgent import SqlAgent
from app.services.agent.SupervisorAgent import SupervisorAgent
from app.services.agent.ResearcherAgent import ResearcherAgent
from app.services.agent.CoderAgent import CoderAgent

class MultiAgentWorkflow:
    """
    Creates and manages a workflow graph connecting multiple agents.
    """
    
    #--------------------------------------------------------------------------------
    # Define the __init__ method to initialize the multi-agent workflow
    #--------------------------------------------------------------------------------
    def __init__(self, model_name="gpt-4o"):
        """
        Initialize the multi-agent workflow.
        
        Args:
            model_name: The LLM model to use for all agents
        """
        self.supervisor_agent = SupervisorAgent(model_name)
        self.researcher_agent = ResearcherAgent(model_name)
        self.coder_agent = CoderAgent(model_name)
        self.sql_agent = SqlAgent(model_name)
        self.members = ["Researcher", "Coder", "SqlAgent"]
        self.graph = None  # Will be initialized when build_graph() is called
    
    #--------------------------------------------------------------------------------
    # Define the build_graph method to build the workflow graph connecting the agents
    #--------------------------------------------------------------------------------
    def build_graph(self):
        """
        Build the workflow graph connecting the agents.
        
        Returns:
            The compiled workflow graph
        """
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent
        workflow.add_node("supervisor", self.supervisor_agent)
        
        # Researcher Agent
        research_node = functools.partial(
            agent_node, agent=self.researcher_agent.agent, name="Researcher"
        )
        workflow.add_node("Researcher", research_node)
        
        # Coder Agent
        code_node = functools.partial(
            agent_node, agent=self.coder_agent.agent, name="Coder"
        )
        workflow.add_node("Coder", code_node)
        
        # SQL Agent
        sql_node = functools.partial(
            agent_node, agent=self.sql_agent.agent, name="SqlAgent"
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
    
    
    
    """
    The functools.partial() creates a new function where:
    - It's based on the agent_node helper function
    - The 'agent' and 'name' parameters are permanently set
    - Only the 'state' parameter will need to be provided when this function is called
    - This makes the node reusable without repeating these arguments
    """