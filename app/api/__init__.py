from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import chatbot_sql_agent, roles, users, courses, role_courses, user_courses, chatbot_sql_agent