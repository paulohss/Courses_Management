from app.models.user import User
from app.models.role import Role
from app import db
from flask import abort

class UserService:
    
    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------        
    def create_user(self, name, role_id):
        # Validation:
        if not name or not name.strip():
            abort(400, 'Name must be provided for a Role!')
        if not role_id or role_id <= 0:
            abort(400, 'Invalid Role ID provided!')                
        role = Role.query.get(role_id)
        if not role:
            abort(400, 'Role ID does not exist!') 
        # Action:
        try:
            new_user = User(name=name, fk_role_id=role_id)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except:
            db.session.rollback()
            raise

    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def get_all_users(self):
        return User.query.all()

    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def get_user_by_id(self, id):
        return User.query.get(id)

    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def update_user(self, id, name, role_id):
        user = self.get_user_by_id(id)
        if user:
            user.name = name
            user.role_id = role_id
            db.session.commit()
        return user

    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def delete_user(self, id):
        user = self.get_user_by_id(id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return user