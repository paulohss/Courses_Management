from app.models.user import User
from app.models.role import Role
from app.models.course import Course 
from app.models.role_course import RoleCourse
from app.models.user_course import UserCourse
from app import db
from flask import abort
from app.utils.logger_service import LoggerService

class UserService:
    
    #-------------------------------------------------------------------------------
    # Constructor
    #-------------------------------------------------------------------------------    
    def __init__(self):
        # Initialize logger
        self.logger = LoggerService.get_instance().get_logger(__name__)            
    
    #-------------------------------------------------------------------------------
    # Validation method
    #-------------------------------------------------------------------------------
    def validate_user(self, name, role_id):
        if not name or not name.strip():
            self.logger.warning('Name must be provided for a User!')
            abort(400, 'Name must be provided for a User!')
            
        if not role_id or role_id <= 0:
            self.logger.warning(f'Invalid Role ID [{role_id}] provided!')
            abort(400, 'Invalid Role ID provided!')
        
        role = Role.query.get(role_id)
        if not role:
            self.logger.warning(f'Role ID [{role_id}] does not exist!')
            abort(400, f'Role ID [{role_id}] does not exist!')



    #-------------------------------------------------------------------------------
    # Create / Add new user
    #-------------------------------------------------------------------------------        
    def create_user(self, name, role_id):
        # Validation:
        self.validate_user(name, role_id)

        # Action:
        try:
            new_user = User(name=name, fk_role_id=role_id)
            db.session.add(new_user)
            db.session.commit()
            return new_user

        except Exception as e:
            self.logger.error(f"Error creating User: {str(e)}")
            db.session.rollback()
            raise



    #-------------------------------------------------------------------------------
    # Get all users
    #-------------------------------------------------------------------------------    
    def get_all_users(self): 
        try:
            return User.query.all()
        except Exception as e:
            self.logger.error(f"Error getting all Users: {str(e)}")  

    #-------------------------------------------------------------------------------
    # Get user by ID
    #-------------------------------------------------------------------------------    
    def get_user_by_id(self, id):
        try:
            if id <= 0:
                self.logger.warning('Invalid User ID provided!')
                abort(400, 'Invalid User ID provided!')
            
            #Get user info
            user = User.query.get(id)
            
            #Get courses attended by user
            user_courses = UserCourse.query\
                .join(Course, UserCourse.fk_course_id == Course.id)\
                .filter(UserCourse.fk_user_id == id)\
                .order_by(Course.name)\
                .all()
                
            courses_attented = [Course.query.get(uc.fk_course_id) for uc in user_courses]
            
            #Get courses available for user
            role_courses = RoleCourse.query\
                .join(Course, RoleCourse.fk_course_id == Course.id)\
                .filter(RoleCourse.fk_role_id == user.fk_role_id)\
                .order_by(Course.name)\
                .all()
                
            courses_avaiable = [Course.query.get(rc.fk_course_id) for rc in role_courses]
            
            # Merge courses_attented and courses_avaiable, avoiding duplicates
            course_ids = set()
            user_course_list = []
            
            for course in courses_attented:
                course_ids.add(course.id)
                user_course_list.append({'id': course.id,'name': course.name,'recurrent': course.recurrent,'attended': True})
                    
            for course in courses_avaiable:
                if course.id not in course_ids:
                    course_ids.add(course.id)
                    user_course_list.append({'id': course.id,'name': course.name,'recurrent': course.recurrent,'attended': False})
            
            if user:
                return {'id': user.id,'name': user.name,'role_id': user.fk_role_id,'role_name': user.role.name,'user_course_list': user_course_list}
            
            return None
        
        except Exception as e:
            self.logger.error(f"Error getting User by ID: {str(e)}")
            raise



    #-------------------------------------------------------------------------------
    # Update user
    #-------------------------------------------------------------------------------    
    def update_user(self, id, name, role_id):
        try:
            # Validation:
            if id <= 0:
                self.logger.warning('Invalid User ID provided!')
                abort(400, 'Invalid User ID provided!')
            
            self.validate_user(name, role_id)
            
            # Action:
            user = User.query.get(id)
            if user:
                user.name = name
                user.fk_role_id = role_id
                db.session.commit()
                return user
            else:
                abort(400, f'User ID [{id}] does not exist!')
        
        except Exception as e:
            self.logger.error(f"Error updating User: {str(e)}")
            db.session.rollback()
            raise


    #-------------------------------------------------------------------------------
    # Delete user
    #-------------------------------------------------------------------------------    
    def delete_user(self, id):
        try:
            if id <= 0:
                self.logger.warning('Invalid User ID provided!')    
                abort(400, 'Invalid User ID provided!')
            
            user = User.query.get(id)
            if user:
                db.session.delete(user)
                db.session.commit()
            else:
                self.logger.warning(f'User ID [{id}] does')
                abort(400, f'User ID [{id}] does not exist!')
            
            return user
        
        except Exception as e:
            self.logger.error(f"Error deleting User: {str(e)}")
            db.session.rollback()
            raise