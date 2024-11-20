from app.models.course import Course
from app import db

class CourseService:
    
    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def create_course(self, name, recurrent):
        new_course = Course(name=name, recurrent=recurrent)
        db.session.add(new_course)
        db.session.commit()
        return new_course

    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def get_all_courses(self):
        return Course.query.all()

    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def get_course_by_id(self, id):
        return Course.query.get(id)

    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def update_course(self, id, name, recurrent):
        course = self.get_course_by_id(id)
        if course:
            course.name = name
            course.recurrent = recurrent
            db.session.commit()
        return course

    #-------------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------------    
    def delete_course(self, id):
        course = self.get_course_by_id(id)
        if course:
            db.session.delete(course)
            db.session.commit()
        return course