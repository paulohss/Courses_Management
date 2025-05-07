from flask import jsonify, request, current_app
from app.api import bp
from app.services.agent.factory.multi_agent_workflow import MultiAgentWorkflow
from langchain_core.messages import HumanMessage
from app.services.llm.llm_setting import LLMConfig
from app.utils.logger_service import LoggerService


#-------------------------------------------------------------------------------
# Initialize logger
#-------------------------------------------------------------------------------
logger = LoggerService.get_instance().get_logger(__name__)


#-------------------------------------------------------------------------------
# Get chatbot service
#-------------------------------------------------------------------------------
def get_chatbot_service():
    try:
        if 'multi_agent_workflow' not in current_app.config:
            
            provider = LLMConfig.PROVIDER
            model =  LLMConfig.MODEL_NAME
            
            logger.info(f"Initializing chatbot service with provider: {provider}, model: {model}")
            
            workflow = MultiAgentWorkflow(provider, model)
            workflow.build_graph()            
            current_app.config['multi_agent_workflow'] = workflow
            
        return current_app.config['multi_agent_workflow']
    
    except Exception as e:
        logger.error(f"Error initializing chatbot service: {str(e)}")



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
        
        # Get the chatbot Singleton Service
        workflow = get_chatbot_service()
        
        # Initialize state with user message
        initial_state = {"messages": [HumanMessage(content=data['message'])]}
        
        # Process the conversation through the graph
        conversation_history = []
        final_response = ""
        chart_data = None
        chart_layout = None
        
        # Process the conversation flow
        for step in workflow.graph.stream(initial_state):            
            logger.info(f"----> Step: {step} <---")
            
            # Skip the end state marker
            if "__end__" in step:
                continue
                
            # Process each agent's response
            for agent_name, response in step.items():
                logger.info(f"--- {agent_name.upper()} Response ---")
                
                # Check for chart data in the response
                if isinstance(response, dict):
                    if "chart_data" in response and "chart_layout" in response:
                        chart_data = response["chart_data"]
                        chart_layout = response["chart_layout"]
                        logger.info(f"Chart data detected from {agent_name}")
                
                # Extract and process the message content based on format
                if isinstance(response, dict) and "messages" in response:
                    # Handle message collection format
                    for message in response["messages"]:
                        message_content = message.content
                        conversation_history.append({"agent": agent_name, "content": message_content})   
                        logger.info(f"Agent: {agent_name}, Content: {message_content}")                     
                        if str(response) != FINISH:
                            final_response = message_content                
                else:                
                    # Handle direct content format                    
                    conversation_history.append({"agent": agent_name, "content": response})                      
                    logger.info(f"Agent: {agent_name}, Content: {response}")
                    if str(response) != FINISH:
                       final_response = response                  
                
                logger.info("---- End of Response ---")

        logger.info("FINAL response: " + final_response)
        
        # Prepare the response object
        response_obj = {'response': final_response}
        
        # Add chart data if available
        if chart_data and chart_layout:
            response_obj['chart'] = {
                'data': chart_data,
                'layout': chart_layout
            }
            
        return jsonify(response_obj), 200

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({'response': 'Internal server error'}), 500




#-------------------------------------------------------------------------------
# Health check endpoint
#-------------------------------------------------------------------------------
@bp.route('/chatbot/health', methods=['GET'])
def health_check():
    try:
        logger.info("Health check requested")
        return jsonify({'status': 'healthy', 'service': 'multi-agent chatbot'}), 200
    
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        return jsonify({'error': 'Service unhealthy', 'details': str(e)}), 500