from app.models.user import User
from app.models.role import Role
from app import db
from flask import abort

class UserService:
    
    #-------------------------------------------------------------------------------
    # Crate / Add new user
    #-------------------------------------------------------------------------------        
    def create_user(self, name, role_id):
        # Validation:
        if not name or not name.strip():
            abort(400, 'Name must be provided for a User!')
            
        if not role_id or role_id <= 0:
            abort(400, 'Invalid Role ID provided!')                
            
        role = Role.query.get(role_id)
        if not role:
            abort(400, f'Role ID [{role_id}] does not exist!') 
        
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
    # Get all users
    #-------------------------------------------------------------------------------    
    def get_all_users(self):
        return User.query.all()

    #-------------------------------------------------------------------------------
    # Get user by ID
    #-------------------------------------------------------------------------------    
    def get_user_by_id(self, id):
        return User.query.get(id)

    #-------------------------------------------------------------------------------
    # Update user
    #-------------------------------------------------------------------------------    
    def update_user(self, id, name, role_id):
        try:
            # Validation:
            if id <= 0:
                abort(400, 'Invalid User ID provided!')            
            if not name or not name.strip():
                abort(400, 'Name must be provided for a User!')

            if role_id <= 0:
                abort(400, 'Invalid Role ID provided!')
            
            role = Role.query.get(role_id)
            if not role:
                abort(400, f'Role ID [{role_id}] does not exist!')
            
            # Action:
            user = self.get_user_by_id(id)
            if user:
                user.name = name
                user.fk_role_id = role_id
                db.session.commit()
                return user
            else:
                abort(400, f'User ID [{id}] does not exist!')  
        
        except:
            db.session.rollback()
            raise

    #-------------------------------------------------------------------------------
    # Delete user
    #-------------------------------------------------------------------------------    
    def delete_user(self, id):
        try:
            if id <= 0:
                abort(400, 'Invalid User ID provided!')
        
            user = self.get_user_by_id(id)
            if user:
                db.session.delete(user)
                db.session.commit()
            else:
                abort(400, f'User ID [{id}] does not exist!')
            
            return user
        
        except:
            db.session.rollback()
            raise   