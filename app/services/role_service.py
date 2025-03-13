from flask import abort
from app.models.role import Role
from app.models.course import Course
from app.models.role_course import RoleCourse
from app import db
from app.utils.logger_service import LoggerService

class RoleService:
    
    #-------------------------------------------------------------------------------
    # Constructor
    #-------------------------------------------------------------------------------    
    def __init__(self):
        # Initialize logger
        self.logger = LoggerService.get_instance().get_logger(__name__)    
    
    #-------------------------------------------------------------------------------
    # Create/Add new Role
    #-------------------------------------------------------------------------------        
    def create_role(self, name):        
        if not name or not name.strip():
            self.logger.warning(f"Role creation failed: Empty name provided")
            abort(400, 'Name must be provided for a Role!')
        try:
            new_role = Role(name=name)
            db.session.add(new_role)
            db.session.commit()
            return new_role
        
        except Exception as e:
            self.logger.error(f"Error creating role '{name}': {str(e)}")
            db.session.rollback()
            raise

            
    #-------------------------------------------------------------------------------
    # Get ALL the Roles
    #-------------------------------------------------------------------------------    
    def get_all_roles(self):
        try:
            return Role.query.all()
        
        except Exception as e:
            self.logger.error(f"Error retrieving roles: {str(e)}")
            raise


    #-------------------------------------------------------------------------------
    # Get Role by ID
    #-------------------------------------------------------------------------------    
    def get_role_by_id(self, id):
        
        try:
            # Validation:
            if id <= 0:
                self.logger.warning(f"Role ID [{id}] is invalid")
                abort(400, 'Invalid User ID provided!')
            
            role = Role.query.get(id)
            if not role:
                self.logger.warning(f"Role ID [{id}] does not exist")
                abort(400, f'Role ID [{id}] does not exist!')
                
            # Get courses linked to role
            role_courses = RoleCourse.query\
                .join(Course, RoleCourse.fk_course_id == Course.id)\
                .filter(RoleCourse.fk_role_id == id)\
                .order_by(Course.name)\
                .all()

            # Get all courses
            all_courses = Course.query.order_by(Course.name).all()
            
            # Initialize final_list
            final_list = []
            
            # Add role_courses to final_list with 'linked' property set to True
            for role_course in role_courses:
                course = Course.query.get(role_course.fk_course_id)
                final_list.append({'id': course.id, 'name': course.name, 'recurrent': course.recurrent, 'linked': True})
                
            # Add all_courses to final_list with 'linked' property set to False, avoiding duplicates
            role_course_ids = {role_course.fk_course_id for role_course in role_courses}
            for course in all_courses:
                if course.id not in role_course_ids:
                    final_list.append({'id': course.id, 'name': course.name, 'recurrent': course.recurrent, 'linked': False})
            
            # Add final_list as a property of role
            role.courses = final_list
            
            return role
        
        except Exception as e:
            self.logger.error(f"Error retrieving role by ID {id}: {str(e)}")
            raise

    #-------------------------------------------------------------------------------
    # Update/Edit a Role
    #-------------------------------------------------------------------------------    
    def update_role(self, id, name):
        if not id or id <= 0:
            self.logger.warning(f"Invalid Role ID provided: {id}")
            abort(400, 'Invalid Role ID provided!')        
        if not name or not name.strip():
            self.logger.warning(f"Role update failed: Empty name provided")
            abort(400, 'Name must be provided for a Role!')
        
        try:
            role = self.get_role_by_id(id)
            if role:
                role.name = name
                db.session.commit()
                return role
            else:
                abort(400, f'Role ID [{id}] does not exist!')
                
        except Exception as e:
            self.logger.error(f"Error updating role '{name}': {str(e)}")
            db.session.rollback()
            raise

            
    #-------------------------------------------------------------------------------
    # Delete a Role
    #-------------------------------------------------------------------------------    
    def delete_role(self, id):
        if not id or id <= 0:
            self.logger.warning(f"Invalid Role ID provided: {id}")
            abort(400, 'Invalid Role ID provided!')     
        
        try:
            role = self.get_role_by_id(id)
            if role:
                db.session.delete(role)
                db.session.commit()
                return role
            else:
                abort(400, f'Role ID [{id}] does not exist')
                
        except Exception as e:
            self.logger.error(f"Error deleting role ID [{id}]: {str(e)}")
            db.session.rollback()
            raise
