from flask import jsonify, request
from app.api import bp
from app.services.role_course_service import RoleCourseService

role_course_service = RoleCourseService()

#-------------------------------------------------------------------------------
# Create a new role-course relationship
#-------------------------------------------------------------------------------
@bp.route('/role_courses', methods=['POST'])
def create_role_course():
    data = request.json
    new_role_course = role_course_service.create_role_course(data['course_id'], data['role_id'])
    return jsonify({'message': 'Role-Course relationship created successfully', 'id': new_role_course.id}), 201


#-------------------------------------------------------------------------------
# Get all role-course relationships
#-------------------------------------------------------------------------------
@bp.route('/role_courses', methods=['GET'])
def get_role_courses():
    role_courses = role_course_service.get_all_role_courses()
    return jsonify([{'id': rc.id, 'course_id': rc.fk_course_id, 'role_id': rc.fk_role_id} for rc in role_courses])


#-------------------------------------------------------------------------------
# Get all courses associated with a role ID
#-------------------------------------------------------------------------------
@bp.route('/role_courses/role/<int:role_id>', methods=['GET'])
def get_courses_by_role_id(role_id):
    courses = role_course_service.get_courses_by_role_id(role_id)
    return jsonify([{'id': course.id, 'name': course.name, 'recurrent': course.recurrent, "attended": False} for course in courses])


#-------------------------------------------------------------------------------
# Update a role-course relationship
#-------------------------------------------------------------------------------
@bp.route('/role_courses/<int:id>', methods=['PUT'])
def update_role_course(id):
    data = request.json
    updated_role_course = role_course_service.update_role_course(id, data['course_id'], data['role_id'])
    if updated_role_course:
        return jsonify({'message': 'Role-Course relationship updated successfully'})
    return jsonify({'message': 'Role-Course relationship not found'}), 404


#-------------------------------------------------------------------------------
# Delete a role-course relationship
#-------------------------------------------------------------------------------
@bp.route('/role_courses', methods=['DELETE'])
def delete_role_course(): 
    data = request.json    
    deleted_role_course = role_course_service.delete_role_course(data['role_id'], data['course_id'])
    if deleted_role_course:
        return jsonify({'message': 'Role-Course relationship deleted successfully'})
    return jsonify({'message': 'Role-Course relationship not found'}), 404


