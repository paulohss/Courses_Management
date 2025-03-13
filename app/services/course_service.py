from app.models.course import Course
from app.models.role_course import RoleCourse
from app.models.role import Role
from flask import abort
from app import db
from app.utils.logger_service import LoggerService

class CourseService:

    #-------------------------------------------------------------------------------
    # Constructor
    #-------------------------------------------------------------------------------    
    def __init__(self):
        # Initialize logger
        self.logger = LoggerService.get_instance().get_logger(__name__)
    
    
    
    #-------------------------------------------------------------------------------
    # Create a new course
    #-------------------------------------------------------------------------------    
    def create_course(self, name, recurrent):
        try:
            # Validation
            if not name or not name.strip():
                self.logger.warning(f"Course creation failed: Empty name provided")
                abort(400, 'Name must be provided for a Course!')
            
            if not len(recurrent.strip()) > 1:
                if recurrent not in ('Annual', 'Quarterty', 'None'):
                    self.logger.warning(f"Course creation failed: Invalid recurrence '{recurrent}'")
                    abort(400, 'Recurrence must be [Annual], [Quarterty] or [None]!')
            
            # Action
            course = Course(name=name, recurrent=recurrent)
            db.session.add(course)
            db.session.commit()
            return course
        
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error creating course '{name}': {str(e)}")
            raise
        
        

    #-------------------------------------------------------------------------------
    # Get all courses
    #-------------------------------------------------------------------------------    
    def get_all_courses(self):
        try:
            return Course.query.all()
        
        except Exception as e:
            self.logger.error(f"Error retrieving courses: {str(e)}")
            raise


    #-------------------------------------------------------------------------------
    # Get a course by id
    #-------------------------------------------------------------------------------    
    def get_course_by_id(self, id): 
        try:
            # Validation:
            if id <= 0:
                abort(400, 'Invalid User ID provided!')
                
            course = Course.query.get(id)
            if not course:
                abort(400, f'Course ID [{id}] does not exist!')     
            
            
            # Get courses linked to role
            role_courses = RoleCourse.query.filter_by(fk_course_id=id).all()
            
            # Get all roles
            all_roles = Role.query.all()
            
            # Initialize final_list
            final_list = []        
            
            # Add role_courses to final_list with 'linked' property set to True
            for role_course in role_courses:
                role = Role.query.get(role_course.fk_role_id)
                final_list.append({'id': role.id, 'name': role.name, 'linked': True})
                
            # Add all_roles to final_list with 'linked' property set to False, avoiding duplicates
            role_course_ids = {role_course.fk_role_id for role_course in role_courses}
            for role in all_roles:
                if role.id not in role_course_ids:
                    final_list.append({'id': role.id, 'name': role.name, 'linked': False})
            
            # Add final_list as a property of course
            course.roles = final_list
            
            return course        
        
        except Exception as e:
            self.logger.error(f"Error retrieving course by ID {id}: {str(e)}")
            raise        
        

    #-------------------------------------------------------------------------------
    # Update a course
    #-------------------------------------------------------------------------------    
    def update_course(self, id, name, recurrent):
        try:
            # Validation
            if id is None or id <= 0:
                abort(400, 'Id must be provided for a Course!')
            
            if not name or not name.strip():
                abort(400, 'Name must be provided for a Course!')
            
            if not len(recurrent.strip()) > 1:
                if recurrent not in ('Annual', 'Quarterty', 'None'):
                    abort(400, 'Recurrence must be [Annual], [Quarterty] or [None]!')
            
            # Action
            course = self.get_course_by_id(id)
            if course:
                course.name = name
                course.recurrent = recurrent
                db.session.commit()
                return course
            else:
                abort(404, f'Course not found for if [{id}]!')
        
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error updating course '{name}': {str(e)}")
            raise

    #-------------------------------------------------------------------------------
    # Delete a course
    #-------------------------------------------------------------------------------    
    def delete_course(self, id):
        try:
            # Validation
            if id is None or id <= 0:
                abort(400, 'Id must be provided for a Course!')

            # Action
            course = self.get_course_by_id(id)
            if course:
                db.session.delete(course)
                db.session.commit()
                return course
            else:
                abort(404, f'Course not found for if [{id}]!')
        
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error deleting course with ID {id}: {str(e)}")
            raise