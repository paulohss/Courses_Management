from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  
    office = db.Column(db.String(50), nullable=False)  
    country = db.Column(db.String(50), nullable=False) 
    fk_role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    user_courses = db.relationship('UserCourse', backref='user', lazy=True)

