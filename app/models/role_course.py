from app import db

class RoleCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fk_course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=False)
    fk_role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=False)