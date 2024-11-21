from flask import abort
from app.models.role import Role
from app import db

class RoleService:
    
    #-------------------------------------------------------------------------------
    # Create/Add new Role
    #-------------------------------------------------------------------------------        
    def create_role(self, name):
        if not name or not name.strip():
            abort(400, 'Name must be provided for a Role!')
        try:
            new_role = Role(name=name)
            db.session.add(new_role)
            db.session.commit()
            return new_role
        except:
            db.session.rollback()
            raise

            
    #-------------------------------------------------------------------------------
    # Get ALL the Roles
    #-------------------------------------------------------------------------------    
    def get_all_roles(self):
        return Role.query.all()

    #-------------------------------------------------------------------------------
    # Get Role by ID
    #-------------------------------------------------------------------------------    
    def get_role_by_id(self, id):
        return Role.query.get(id)

    #-------------------------------------------------------------------------------
    # Update/Edit a Role
    #-------------------------------------------------------------------------------    
    def update_role(self, id, name):
        if not id or id <= 0:
            abort(400, 'Invalid Role ID provided!')        
        if not name or not name.strip():
            abort(400, 'Name must be provided for a Role!')
        
        try:
            role = self.get_role_by_id(id)
            if role:
                role.name = name
                db.session.commit()
            return role
        except:
            db.session.rollback()
            raise

            
    #-------------------------------------------------------------------------------
    # Delete a Role
    #-------------------------------------------------------------------------------    
    def delete_role(self, id):
        if not id or id <= 0:
            abort(400, 'Invalid Role ID provided!')     
        
        try:
            role = self.get_role_by_id(id)
            if role:
                db.session.delete(role)
                db.session.commit()
            return role
        except:
            db.session.rollback()
            raise
