import json
from langchain_core.messages import HumanMessage
from services.agent.Factory.MultiAgentWorkflow import MultiAgentWorkflow


# ---------------------------------------------------------
# Run Multi-Agent Workflow
# ---------------------------------------------------------
def run_multi_agent(query: str, model_name: str = "gpt-4o"):

    workflow = MultiAgentWorkflow(model_name)
    graph = workflow.build_graph()
    
    # Process the user query
    conversation_history = []
    
    # Start with the user's initial query
    initial_state = {"messages": [HumanMessage(content=query)]}
    
    # Process the conversation flow
    for step in graph.stream(initial_state):
        # Skip the end state marker
        if "__end__" in step:
            continue
            
        # Process each agent's response
        for agent_name, response in step.items():
            print(f"\n--- {agent_name.upper()} Response ---")
            
            # Extract and process the message content based on format
            if isinstance(response, dict) and "messages" in response: # check if response is a dict and has a "messages" key
                # Handle message collection format
                for message in response["messages"]:
                    message_content = message.content
                    print(message_content)
                    conversation_history.append({
                        "agent": agent_name,
                        "content": message_content
                    })
            else:
                # Handle direct content format
                print(json.dumps(response, indent=2))
                conversation_history.append({
                    "agent": agent_name, 
                    "content": response
                })
                
            print("\n---- End of Response ---")
    
    return conversation_history



# Entry point
#--------------------------------------------------------------------------------
if __name__ == "__main__":
    query = input("Enter your query: ")
    results = run_multi_agent(query)