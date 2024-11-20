from app.models.user import User
from app import db

class UserService:
    
    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------        
    def create_user(self, name, role_id):
        new_user = User(name=name, role_id=role_id)
        db.session.add(new_user)
        db.session.commit()
        return new_user

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