from app import db

class UserCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fk_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fk_course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
     