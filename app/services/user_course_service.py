from app.models.user_course import UserCourse
from app import db

class UserCourseService:
    
    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def create_user_course(self, user_id, course_id):
        new_user_course = UserCourse(user_id=user_id, course_id=course_id)
        db.session.add(new_user_course)
        db.session.commit()
        return new_user_course

    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def get_all_user_courses(self):
        return UserCourse.query.all()


    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def delete_user_course(self, id):
        user_course = UserCourse.query.get(id)
        if user_course:
            db.session.delete(user_course)
            db.session.commit()
        return user_course