from app.models.course import Course
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
        return Course.query.get(id)

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
