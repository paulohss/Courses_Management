from langchain_core.messages import HumanMessage
from app.utils.logger_service import LoggerService

# --------------------------------------------------------------------------------
# Initialize logger
# --------------------------------------------------------------------------------
logger = LoggerService.get_instance().get_logger(__name__)


# --------------------------------------------------------------------------------
# Invocation Wrapper
# --------------------------------------------------------------------------------
def agent_node(state, agent, name):
    """
    Wraps an agent's invocation and formats its response as a HumanMessage
    with the agent's name.
    """
    try:
        logger.info(f"Invoking agent: {name}")
        result = agent.invoke(state)
        logger.info(f"Agent {name} result type: {type(result)}")
        
        # Extract messages from result
        if isinstance(result, dict) and "messages" in result:
            messages = result.get("messages")
            chart_data = result.get("chart_data")
            chart_layout = result.get("chart_layout")
            if messages and len(messages) > 0:
                # Check if the message has chart attributes
                message = messages[-1]
                if chart_data is not None and chart_layout is not None:
                    logger.info(f"Chart data found in {name} response")
                    return {
                        "messages": [HumanMessage(content=message.content, name=name)],
                        "next": "FINISH",
                        "chart_data": chart_data,
                        "chart_layout": chart_layout
                    }
                else:
                    logger.info(f"{name} response found")
                    return {
                        "messages": [HumanMessage(content=message.content, name=name)],
                        "next": "FINISH"
                    }
        
        # Fallback for unexpected formats
        logger.warning(f"Unexpected result format from {name}")
        return {
            "messages": [HumanMessage(content=f"Unexpected result format from {name}", name=name)], 
            "next": "FINISH"
            }
        
    except Exception as e:
        logger.error(f"Error invoking agent {name}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            "messages": [HumanMessage(content=f"Error in {name}: {str(e)}", name=name)],
            "next": "FINISH"
        }