from flask import jsonify, request
from app.api import bp
from app.services.role_course_service import RoleCourseService

role_course_service = RoleCourseService()

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
@bp.route('/role_courses', methods=['POST'])
def create_role_course():
    data = request.json
    new_role_course = role_course_service.create_role_course(data['course_id'], data['role_id'])
    return jsonify({'message': 'Role-Course relationship created successfully'}), 201


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
@bp.route('/role_courses', methods=['GET'])
def get_role_courses():
    role_courses = role_course_service.get_all_role_courses()
    return jsonify([{'course_id': rc.course_id, 'role_id': rc.role_id} for rc in role_courses])


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
@bp.route('/role_courses', methods=['DELETE'])
def delete_role_course():
    data = request.json
    deleted_role_course = role_course_service.delete_role_course(data['course_id'], data['role_id'])
    if deleted_role_course:
        return jsonify({'message': 'Role-Course relationship deleted successfully'})
    return jsonify({'message': 'Role-Course relationship not found'}), 404