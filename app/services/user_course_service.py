from app.models.user_course import UserCourse
from app.models.user import User
from app.models.course import Course
from app import db
from flask import abort

class UserCourseService:
    
    #-------------------------------------------------------------------------------
    # Validation method
    #-------------------------------------------------------------------------------
    def validate_user_and_course(self, user_id, course_id):
        if not user_id or user_id <= 0:
            abort(400, 'Invalid User ID provided!')
        
        if not course_id or course_id <= 0:
            abort(400, 'Invalid Course ID provided!')
        
        user = User.query.get(user_id)
        if not user:
            abort(400, f'User ID [{user_id}] does not exist!')
        
        course = Course.query.get(course_id)
        if not course:
            abort(400, f'Course ID [{course_id}] does not exist!')
 

    #-------------------------------------------------------------------------------
    # Create / Add new user-course relationship
    #-------------------------------------------------------------------------------    
    def create_user_course(self, user_id, course_id):
        
        # Validation:
        self.validate_user_and_course(user_id, course_id)

        # Action:
        try:
            new_user_course = UserCourse(fk_user_id=user_id, fk_course_id=course_id)
            db.session.add(new_user_course)
            db.session.commit()
            return new_user_course
        except:
            db.session.rollback()
            raise

    #-------------------------------------------------------------------------------
    # Get all user-course relationships
    #-------------------------------------------------------------------------------    
    def get_all_user_courses(self):
        return UserCourse.query.all()


    #-------------------------------------------------------------------------------
    # Get all courses associated with a user ID
    #-------------------------------------------------------------------------------    
    def get_courses_by_user_id(self, user_id):
        if not user_id or user_id <= 0:
            abort(400, 'Invalid User ID provided!')
        
        user_courses = UserCourse.query.filter_by(fk_user_id=user_id).all()
        courses = [Course.query.get(uc.fk_course_id) for uc in user_courses]
        return courses


    #-------------------------------------------------------------------------------
    # Update user-course relationship
    #-------------------------------------------------------------------------------    
    def update_user_course(self, user_id, course_id):
        try:
            # Validation:
            if id <= 0:
                abort(400, 'Invalid User-Course Relationship ID provided!')
            
            self.validate_user_and_course(user_id, course_id)
            
            # Action:
            user_course = UserCourse.query.filter_by(fk_user_id=user_id, fk_course_id=course_id).first()
            if user_course:
                user_course.fk_user_id = user_id
                user_course.fk_course_id = course_id
                db.session.commit()
            else:
                abort(400, f'User-Course Relationship does not exist!')
            
            return user_course
        except:
            db.session.rollback()
            raise
    
        
    #-------------------------------------------------------------------------------
    # Get user-course relationship by ID
    #-------------------------------------------------------------------------------    
    def delete_user_course(self, user_id, course_id):
        
        # Validation:
        self.validate_user_and_course(user_id, course_id)
        
        try:
            # Action:
            user_course = UserCourse.query.filter_by(fk_user_id=user_id, fk_course_id=course_id).first()
            if user_course:
                db.session.delete(user_course)
                db.session.commit()
            else:
                abort(400, f'User-Course Relationship does not exist!')
            
            return user_course
        except:
            db.session.rollback()
            raise