from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from klk.models import User, Student
import email_validator

class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(min=2 , max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username is taken, choose a different username.')
        
    def email_validator(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('The email is taken, choose a different email.')

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(min=2 , max=20)])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class StudentForm(FlaskForm):
    studentname = StringField('Student Name:', validators=[DataRequired(), Length(min=2 , max=20)])
    school = StringField('School:', validators=[DataRequired(), Length(min=2 , max=20)])
    year = StringField('Year in/Class/Form:', validators=[DataRequired()])
    course = StringField('Course Taking:', validators=[DataRequired(), Length(min=2 , max=20)])
    description = TextAreaField('Description:', validators=[DataRequired()])
    picture = FileField('Upload student picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')

    


