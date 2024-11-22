from app import db

class RoleCourse(db.Model):
    fk_course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    fk_role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)