from flask import jsonify, request
from app.api import bp
from app.services.course_service import CourseService

course_service = CourseService()


#-------------------------------------------------------------------------------
#  Create a new course
#-------------------------------------------------------------------------------
@bp.route('/courses', methods=['POST'])
def create_course():
    data = request.json
    new_course = course_service.create_course(data['name'], data['recurrent'])
    return jsonify({'message': 'Course created successfully', 'id': new_course.id}), 201


#-------------------------------------------------------------------------------
# Get all courses
#-------------------------------------------------------------------------------
@bp.route('/courses', methods=['GET'])
def get_courses():
    courses = course_service.get_all_courses()
    return jsonify([{'id': course.id, 'name': course.name, 'recurrent': course.recurrent} for course in courses])


#-------------------------------------------------------------------------------
# Get a course by id
#-------------------------------------------------------------------------------
@bp.route('/courses/<int:id>', methods=['GET'])
def get_courses_by_id(id): 
    course = course_service.get_course_by_id(id)
    return jsonify({'id': course.id, 'name': course.name, 'recurrent': course.recurrent, 'rolesList': course.roles})

#-------------------------------------------------------------------------------
# Get a course by id
#-------------------------------------------------------------------------------
@bp.route('/courses/<int:id>', methods=['PUT'])
def update_course(id):
    data = request.json
    updated_course = course_service.update_course(id, data['name'], data['recurrent'])
    if updated_course:
        return jsonify({'message': 'Course updated successfully'})
    return jsonify({'message': 'Course not found'}), 404


#-------------------------------------------------------------------------------
# Get a course by id
#-------------------------------------------------------------------------------
@bp.route('/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    deleted_course = course_service.delete_course(id)
    if deleted_course:
        return jsonify({'message': 'Course deleted successfully'})
    return jsonify({'message': 'Course not found'}), 404