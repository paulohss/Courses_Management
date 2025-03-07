from flask import jsonify, request, current_app
from app.api import bp
from app.services.agent.sql_agent import sql_agent


#-------------------------------------------------------------------------------
# Get chatbot service
#-------------------------------------------------------------------------------
def get_chatbot_service():
    if 'chatbot_service' not in current_app.config:
        current_app.config['chatbot_service'] = sql_agent()
    return current_app.config['chatbot_service']


#-------------------------------------------------------------------------------
# Process chat message
#-------------------------------------------------------------------------------
@bp.route('/sqlchatbot/ask', methods=['POST'])
def process_message():
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        chatbot_service = get_chatbot_service()
        response = chatbot_service.execute_query(data['message'])

        return jsonify({'response': response}), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


#-------------------------------------------------------------------------------
# Health check endpoint
#-------------------------------------------------------------------------------
@bp.route('/sqlchatbot/health', methods=['GET'])
def health_check():
    try:
        return jsonify({'status': 'healthy', 'service': 'chatbot'}), 200
    except Exception as e:
        return jsonify({'error': 'Service unhealthy', 'details': str(e)}), 500