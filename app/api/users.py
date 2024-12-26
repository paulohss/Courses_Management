from flask import jsonify, request
from app.api import bp
from app.services.user_service import UserService

user_service = UserService()

#-------------------------------------------------------------------------------
# Create new user
#-------------------------------------------------------------------------------
@bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'name' not in data or 'role_id' not in data:
        return jsonify({'message': 'Invalid data'}), 400
    new_user = user_service.create_user(data['name'], data['role_id'])
    return jsonify({'message': 'User created successfully', 'id': new_user.id}), 201

#-------------------------------------------------------------------------------
# Get all users
#-------------------------------------------------------------------------------
@bp.route('/users', methods=['GET'])
def get_users():
    users = user_service.get_all_users()
    return jsonify([
        {
            'id': user.id,
            'name': user.name,
            'role': {
                'id': user.role.id,
                'name': user.role.name
            }
        }
        for user in users
    ])

#-------------------------------------------------------------------------------
# Get a users by id 
#-------------------------------------------------------------------------------
@bp.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = user_service.get_user_by_id(id)
    if user:
        return jsonify({
            'id': user['id'],
            'name': user['name'],
            'role': {
                'id': user['role_id'],
                'name': user['role_name']
            },
            'userCourseList': user['user_course_list']
        })
    return jsonify({'message': 'User not found'}), 404

#-------------------------------------------------------------------------------
# Update user
#-------------------------------------------------------------------------------
@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    if not data or 'name' not in data or 'role_id' not in data:
        return jsonify({'message': 'Invalid data'}), 400
    
    updated_user = user_service.update_user(id, data['name'], data['role_id'])
    if updated_user:
        return jsonify({'message': 'User updated successfully'})
    return jsonify({'message': 'User not found'}), 404

#-------------------------------------------------------------------------------
# Delete user
#-------------------------------------------------------------------------------
@bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    deleted_user = user_service.delete_user(id)
    if deleted_user:
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'message': 'User not found'}), 404