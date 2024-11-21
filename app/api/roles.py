from flask import jsonify, request
from app.api import bp
from app.services.role_service import RoleService

role_service = RoleService()

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
@bp.route('/roles', methods=['POST'])
def create_role():
    data = request.json
    new_role = role_service.create_role(data['name'])
    return jsonify({'message': 'Role created successfully', 'id': new_role.id}), 201

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
@bp.route('/roles', methods=['GET'])
def get_roles():
    roles = role_service.get_all_roles()
    return jsonify([{'id': role.id, 'name': role.name} for role in roles])


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
@bp.route('/roles/<int:id>', methods=['PUT'])
def update_role(id):
    data = request.json
    updated_role = role_service.update_role(id, data['name'])
    if updated_role:
        return jsonify({'message': 'Role updated successfully'})
    return jsonify({'message': f'Role not found for ID [{id}'}), 404


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
@bp.route('/roles/<int:id>', methods=['DELETE'])
def delete_role(id):
    deleted_role = role_service.delete_role(id)
    if deleted_role:
        return jsonify({'message': 'Role deleted successfully'})
    return jsonify({'message': 'Role not found'}), 404