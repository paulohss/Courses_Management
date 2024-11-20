from flask import jsonify, request
from app.api import bp
from app.services.user_course_service import UserCourseService

user_course_service = UserCourseService()



#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
@bp.route('/user_courses', methods=['POST'])
def create_user_course():
    data = request.json
    new_user_course = user_course_service.create_user_course(data['user_id'], data['course_id'])
    return jsonify({'message': 'User-Course relationship created successfully', 'id': new_user_course.id}), 201


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
@bp.route('/user_courses', methods=['GET'])
def get_user_courses():
    user_courses = user_course_service.get_all_user_courses()
    return jsonify([{'id': uc.id, 'user_id': uc.user_id, 'course_id': uc.course_id} for uc in user_courses])


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
@bp.route('/user_courses/<int:id>', methods=['DELETE'])
def delete_user_course(id):
    deleted_user_course = user_course_service.delete_user_course(id)
    if deleted_user_course:
        return jsonify({'message': 'User-Course relationship deleted successfully'})
    return jsonify({'message': 'User-Course relationship not found'}), 404