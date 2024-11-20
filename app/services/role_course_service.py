from app.models.role_course import RoleCourse
from app import db

class RoleCourseService:
    
    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------        
    def create_role_course(self, course_id, role_id):
        new_role_course = RoleCourse(course_id=course_id, role_id=role_id)
        db.session.add(new_role_course)
        db.session.commit()
        return new_role_course

    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def get_all_role_courses(self):
        return RoleCourse.query.all()

    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def delete_role_course(self, course_id, role_id):
        role_course = RoleCourse.query.filter_by(course_id=course_id, role_id=role_id).first()
        if role_course:
            db.session.delete(role_course)
            db.session.commit()
        return role_course