from app import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    recurrent = db.Column(db.String(50), nullable=False)
    role_courses = db.relationship('RoleCourse', backref='course', lazy=True)
    user_courses = db.relationship('UserCourse', backref='course', lazy=True)