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
    def validate_user(self, name, role_id, email, id, office, country):
        
        if not name or not name.strip():
            self.logger.warning('Name must be provided for a User!')
            abort(400, 'Name must be provided for a User!')
           
        if not office or not office.strip():
            self.logger.warning('Office must be provided for a User!')
            abort(400, 'Office must be provided for a User!')

        if not country or not country.strip():
            self.logger.warning('Country must be provided for a User!')
            abort(400, 'Country must be provided for a User!')            

        if not email or not email.strip():
            self.logger.warning('Email must be provided for a User!')
            abort(400, 'Email must be provided for a User!')
        
        if '@' not in email or '.' not in email:
            self.logger.warning(f'Invalid email format: {email}')
            abort(400, 'Invalid email format!')
        
        # TODO: Check if email already exists in the database
                    
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
    def create_user(self, name, role_id, email, office, country):
        
        # Validation:
        self.validate_user(name, role_id, email, 0, office, country)

        # Action:
        try:
            new_user = User(name=name, fk_role_id=role_id, email=email, office=office, country=country)
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
    # Helper method to fetch user details and courses
    #-------------------------------------------------------------------------------
    def _get_user_details(self, user):
        if not user:
            return None

        # Get courses attended by user
        user_courses = UserCourse.query \
            .join(Course, UserCourse.fk_course_id == Course.id) \
            .filter(UserCourse.fk_user_id == user.id) \
            .order_by(Course.name) \
            .all()

        courses_attended = [Course.query.get(uc.fk_course_id) for uc in user_courses]

        # Get courses available for user
        role_courses = RoleCourse.query \
            .join(Course, RoleCourse.fk_course_id == Course.id) \
            .filter(RoleCourse.fk_role_id == user.fk_role_id) \
            .order_by(Course.name) \
            .all()

        courses_available = [Course.query.get(rc.fk_course_id) for rc in role_courses]

        # Merge courses_attended and courses_available, avoiding duplicates
        course_ids = set()
        user_course_list = []

        for course in courses_attended:
            course_ids.add(course.id)
            user_course_list.append({
                'id': course.id,
                'name': course.name,
                'recurrent': course.recurrent,
                'attended': True
            })

        for course in courses_available:
            if course.id not in course_ids:
                course_ids.add(course.id)
                user_course_list.append({
                    'id': course.id,
                    'name': course.name,
                    'recurrent': course.recurrent,
                    'attended': False
                })

        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'office': user.office,
            'country': user.country,
            'role_id': user.fk_role_id,
            'role_name': user.role.name,
            'user_course_list': user_course_list
        }

    #-------------------------------------------------------------------------------
    # Get user by ID
    #-------------------------------------------------------------------------------    
    def get_user_by_id(self, id):
        try:
            if id <= 0:
                self.logger.warning('Invalid User ID provided!')
                abort(400, 'Invalid User ID provided!')
            
            user = User.query.get(id)
            return self._get_user_details(user)
        
        except Exception as e:
            self.logger.error(f"Error getting User by ID: {str(e)}")
            raise


    #-------------------------------------------------------------------------------
    # Get user by Name
    #-------------------------------------------------------------------------------    
    def get_user_by_name(self, name):
        try:
            if not name or not name.strip():
                self.logger.warning('Name must be provided for a User!')
                abort(400, 'Name must be provided for a User!')
                                    
            user = User.query.filter(User.name.ilike(f"%{name}%")).first()
            return self._get_user_details(user)
        
        except Exception as e:
            self.logger.error(f"Error getting User by Name: {str(e)}")
            raise


    #-------------------------------------------------------------------------------
    # Update user
    #-------------------------------------------------------------------------------    
    def update_user(self, id, name, role_id, email, office, country):
        try:
            # Validation:
            if id <= 0:
                self.logger.warning('Invalid User ID provided!')
                abort(400, 'Invalid User ID provided!')
            
            self.validate_user(name, role_id, email, id, office, country)
            
            # Action:
            user = User.query.get(id)
            if user:
                user.name = name
                user.fk_role_id = role_id
                user.email = email
                user.office = office
                user.country = country
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