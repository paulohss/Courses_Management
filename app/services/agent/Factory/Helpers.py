from langchain_core.messages import HumanMessage

def agent_node(state, agent, name):
    """
    Wraps an agent's invocation and formats its response as a HumanMessage
    with the agent's name.
    
    Args:
        state: The current state containing messages
        agent: The agent to invoke
        name: The name of the agent, to be included in the response
        
    Returns:
        Dict with messages field containing the agent's response
    """
    result = agent.invoke(state)
    return {
        "messages": [HumanMessage(content=result["messages"][-1].content, name=name)]
    }