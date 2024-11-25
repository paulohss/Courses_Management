from flask import jsonify, request
from app.api import bp
from app.services.user_course_service import UserCourseService

user_course_service = UserCourseService()



#-------------------------------------------------------------------------------
# Create / Add new user-course relationship
#-------------------------------------------------------------------------------
@bp.route('/user_courses', methods=['POST'])
def create_user_course():
    data = request.json
    new_user_course = user_course_service.create_user_course(data['user_id'], data['course_id'])
    return jsonify({'message': 'User-Course relationship created successfully', 'id': new_user_course.id}), 201


#-------------------------------------------------------------------------------
# Get all user-course relationships
#-------------------------------------------------------------------------------
@bp.route('/user_courses', methods=['GET'])
def get_user_courses():
    user_courses = user_course_service.get_all_user_courses()
    return jsonify([{'id': uc.id, 'user_id': uc.fk_user_id, 'course_id': uc.fk_course_id} for uc in user_courses])


#-------------------------------------------------------------------------------
# Get user-course relationship by ID
#-------------------------------------------------------------------------------
@bp.route('/user_courses/<int:id>', methods=['PUT'])
def update_user_course(id):
    data = request.json
    updated_user_course = user_course_service.update_user_course(id, data['user_id'], data['course_id'])
    if updated_user_course:
        return jsonify({'message': 'User-Course relationship updated successfully'})
    return jsonify({'message': 'User-Course relationship not found'}), 404

#-------------------------------------------------------------------------------
# Delete user-course relationship by ID
#-------------------------------------------------------------------------------
@bp.route('/user_courses/<int:id>', methods=['DELETE'])
def delete_user_course(id):
    deleted_user_course = user_course_service.delete_user_course(id)
    if deleted_user_course:
        return jsonify({'message': 'User-Course relationship deleted successfully'})
    return jsonify({'message': 'User-Course relationship not found'}), 404