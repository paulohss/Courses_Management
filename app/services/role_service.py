from app.models.role import Role
from app import db

class RoleService:
    
    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------        
    def create_role(self, name):
        new_role = Role(name=name)
        db.session.add(new_role)
        db.session.commit()
        return new_role

    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def get_all_roles(self):
        return Role.query.all()

    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def get_role_by_id(self, id):
        return Role.query.get(id)

    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def update_role(self, id, name):
        role = self.get_role_by_id(id)
        if role:
            role.name = name
            db.session.commit()
        return role

    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def delete_role(self, id):
        role = self.get_role_by_id(id)
        if role:
            db.session.delete(role)
            db.session.commit()
        return role