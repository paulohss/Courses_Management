from app.models.course import Course
from app.models.role_course import RoleCourse
from app.models.role import Role
from flask import abort
from app import db

class CourseService:
    
    #-------------------------------------------------------------------------------
    # Create a new course
    #-------------------------------------------------------------------------------    
    def create_course(self, name, recurrent):
        try:
            # Validation
            if not name or not name.strip():
                abort(400, 'Name must be provided for a Course!')
            
            if not len(recurrent.strip()) > 1:
                if recurrent not in ('Annual', 'Quarterty', 'None'):
                    abort(400, 'Recurrence must be [Annual], [Quarterty] or [None]!')
            
            # Action
            course = Course(name=name, recurrent=recurrent)
            db.session.add(course)
            db.session.commit()
            return course
        
        except:
            db.session.rollback()
            raise

    #-------------------------------------------------------------------------------
    # Get all courses
    #-------------------------------------------------------------------------------    
    def get_all_courses(self):
        return Course.query.all()

    #-------------------------------------------------------------------------------
    # Get a course by id
    #-------------------------------------------------------------------------------    
    def get_course_by_id(self, id): 
        
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
        
        

    #-------------------------------------------------------------------------------
    # Update a course
    #-------------------------------------------------------------------------------    
    def update_course(self, id, name, recurrent):
        
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

    #-------------------------------------------------------------------------------
    # Delete a course
    #-------------------------------------------------------------------------------    
    def delete_course(self, id):
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
