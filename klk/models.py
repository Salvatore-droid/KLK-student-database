from datetime import datetime
from klk import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def user_load(student_id):
    return User.query.get(int(student_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image = db.Column(db.String(20),  nullable=False, default='KLK_Logo.jpg')
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    students = db.relationship('Student', backref='name', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image}')"

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentname = db.Column(db.String(20), nullable=False)
    school = db.Column(db.String(120), nullable=False)
    year = db.Column(db.String, nullable=False)
    course = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    results = db.Column(db.Integer, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"User('{self.studentname}', '{self.school}', '{self.year}', '{self.course}', '{self.results}', '{self.descrition}')"

