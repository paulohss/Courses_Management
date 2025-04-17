from app.models.role_course import RoleCourse
from app.models.role import Role
from app.models.course import Course
from app import db
from flask import abort
from app.utils.logger_service import LoggerService

class RoleCourseService:

    #-------------------------------------------------------------------------------
    # Constructor
    #-------------------------------------------------------------------------------    
    def __init__(self):
        # Initialize logger
        self.logger = LoggerService.get_instance().get_logger(__name__)
    
    
    #-------------------------------------------------------------------------------
    # Validation method
    #-------------------------------------------------------------------------------
    def validate_role_and_course(self, role_id, course_id):
        try:
            if not role_id or role_id <= 0:
                abort(400, 'Invalid Role ID provided!')
            
            if not course_id or course_id <= 0:
                abort(400, 'Invalid Course ID provided!')
            
            role = Role.query.get(role_id)
            if not role:
                abort(400, f'Role ID [{role_id}] does not exist!')
            
            course = Course.query.get(course_id)
            if not course:
                abort(400, f'Course ID [{course_id}] does not exist!')
        
        except Exception as e:
            self.logger.error(f"Error validating role and course: {str(e)}")
            raise

    #-------------------------------------------------------------------------------
    # Create a new role-course relationship
    #-------------------------------------------------------------------------------        
    def create_role_course(self, course_id, role_id):
        try:
            # Validation:
            self.validate_role_and_course(role_id, course_id)

            # Action:
            try:
                new_role_course = RoleCourse(fk_course_id=course_id, fk_role_id=role_id)
                db.session.add(new_role_course)
                db.session.commit()
                return new_role_course
            except:
                db.session.rollback()
                raise
            
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error creating role-course relationship: {str(e)}")


    #-------------------------------------------------------------------------------
    # Get all role-course relationships
    #-------------------------------------------------------------------------------    
    def get_all_role_courses(self):
        try:
            return RoleCourse.query.all() 
        except Exception as e:
            self.logger.error(f"Error retrieving role-courses: {str(e)}")



    #-------------------------------------------------------------------------------
    # Get all courses associated with a role ID
    #-------------------------------------------------------------------------------    
    def get_courses_by_role_id(self, role_id):
        try:
            if not role_id or role_id <= 0:
                self.logger.warning(f"Invalid Role ID provided: {role_id}")
                abort(400, 'Invalid Role ID provided!')
            
            role_courses = RoleCourse.query.filter_by(fk_role_id=role_id).all()
            courses = [Course.query.get(rc.fk_course_id) for rc in role_courses]
            return courses
        
        except Exception as e:
            self.logger.error(f"Error retrieving courses by role ID: {str(e)}")




    #-------------------------------------------------------------------------------
    # Delete a role-course relationship
    #-------------------------------------------------------------------------------    
    def delete_role_course(self, role_id, course_id):
        try:
            # Validation:
            self.validate_role_and_course(role_id, course_id)
            
            # Action:
            role_course = RoleCourse.query.filter_by(fk_course_id=course_id, fk_role_id=role_id).first()
            if role_course:
                db.session.delete(role_course)
                db.session.commit()
            else:
                abort(400, f'Role-Course relationship with ID [{id}] does not exist!')
            
            return role_course
        
        except Exception as e:
            self.logger.error(f"Error deleting role-course relationship: {str(e)}")
            db.session.rollback()
            raise

    #-------------------------------------------------------------------------------
    # Update a role-course relationship
    #-------------------------------------------------------------------------------    
    def update_role_course(self, id, new_course_id, new_role_id):
        try:
            # Validation:
            if id <= 0:
                abort(400, 'Invalid Course-Role Relationship ID provided!')
                
            self.validate_role_and_course(new_role_id, new_course_id)
            
            # Action:
            role_course = RoleCourse.query.get(id)
            if role_course:
                role_course.fk_course_id = new_course_id
                role_course.fk_role_id = new_role_id
                db.session.commit()
            else:
                abort(400, f'Role-Course relationship with Course ID [{new_course_id}] and Role ID [{new_role_id}] does not exist!')
            
            return role_course
        
        except Exception as e:
            self.logger.error(f"Error deleting role-course relationship: {str(e)}")
            db.session.rollback()
            raise