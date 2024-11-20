from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import roles, users, courses, role_courses, user_courses