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
    new_user = user_service.create_user(data['name'], data['role_id'])
    return jsonify({'message': 'User created successfully', 'id': new_user.id}), 201

#-------------------------------------------------------------------------------
# Get all users
#-------------------------------------------------------------------------------
@bp.route('/users', methods=['GET'])
def get_users():
    users = user_service.get_all_users()
    return jsonify([{'id': user.id, 'name': user.name, 'role_id': user.fk_role_id} for user in users])

#-------------------------------------------------------------------------------
# Get a users by id
#-------------------------------------------------------------------------------
@bp.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = user_service.get_user_by_id(id)
    return jsonify({'id': user.id, 'name': user.name, 'role_id': user.fk_role_id})

#-------------------------------------------------------------------------------
# Update user
#-------------------------------------------------------------------------------
@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
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