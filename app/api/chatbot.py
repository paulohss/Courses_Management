from flask import jsonify, request, current_app
from app.api import bp
from app.services.agent.Factory.MultiAgentWorkflow import MultiAgentWorkflow
from langchain_core.messages import HumanMessage


#-------------------------------------------------------------------------------
# Get chatbot service
#-------------------------------------------------------------------------------
def get_chatbot_service():
    if 'multi_agent_workflow' not in current_app.config:
        # Initialize the multi-agent workflow
        workflow = MultiAgentWorkflow()
        # Build the graph
        workflow.build_graph()
        current_app.config['multi_agent_workflow'] = workflow
    return current_app.config['multi_agent_workflow']


#-------------------------------------------------------------------------------
# Process chat message
#-------------------------------------------------------------------------------
@bp.route('/chatbot/ask', methods=['POST'])
def process_message():
    try:
        FINISH = "{'next': 'FINISH'}"
        
        data = request.json
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        workflow = get_chatbot_service()
        
        # Initialize state with user message
        initial_state = {"messages": [HumanMessage(content=data['message'])]}
        
        # Process the conversation through the graph
        conversation_history = []
        final_response = ""
        
        # Process the conversation flow
        for step in workflow.graph.stream(initial_state):
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
                        
                        if response != FINISH:
                            final_response = message_content
                
                else:
                
                    # Handle direct content format
                    print(jsonify(response))
                    conversation_history.append({
                        "agent": agent_name, 
                        "content": response
                    })  
                    
                    if str(response) != FINISH:
                       final_response = response                  
                
                print("\n---- End of Response ---")

        return jsonify({'response': final_response}), 200


    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


#-------------------------------------------------------------------------------
# Health check endpoint
#-------------------------------------------------------------------------------
@bp.route('/chatbot/health', methods=['GET'])
def health_check():
    try:
        return jsonify({'status': 'healthy', 'service': 'multi-agent chatbot'}), 200
    except Exception as e:
        return jsonify({'error': 'Service unhealthy', 'details': str(e)}), 500