from app.models.role_course import RoleCourse
from app.models.role import Role
from app.models.course import Course
from app import db
from flask import abort

class RoleCourseService:
    
    #-------------------------------------------------------------------------------
    # Validation method
    #-------------------------------------------------------------------------------
    def validate_role_and_course(self, role_id, course_id):
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

    #-------------------------------------------------------------------------------
    # Create a new role-course relationship
    #-------------------------------------------------------------------------------        
    def create_role_course(self, course_id, role_id):
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

    #-------------------------------------------------------------------------------
    # Get all role-course relationships
    #-------------------------------------------------------------------------------    
    def get_all_role_courses(self):
        return RoleCourse.query.all()

    #-------------------------------------------------------------------------------
    # Delete a role-course relationship
    #-------------------------------------------------------------------------------    
    def delete_role_course(self, id):
        try:
            # Validation:
            if id <= 0:
                abort(400, 'Invalid Role-Course Relationship ID provided!')
            
            # Action:
            role_course = RoleCourse.query.get(id)
            if role_course:
                db.session.delete(role_course)
                db.session.commit()
            else:
                abort(400, f'Role-Course relationship with ID [{id}] does not exist!')
            
            return role_course
        except:
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
        except:
            db.session.rollback()
            raise