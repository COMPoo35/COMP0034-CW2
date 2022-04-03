from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from wtforms import BooleanField
from flask_wtf.file import FileField, FileAllowed
from my_app import photos
from my_app.models import User, Profile


def validate_signup_email(self, email):
    users = User.query.filter_by(email=email.data).first()
    if users is not None:
        raise ValidationError('An account is already registered for that email address')


class SignupForm(FlaskForm):
    title = SelectField(label='Title', validators=[DataRequired()], choices=[
        ('Mr', 'Mr'), ('Ms', 'Ms'), ('Dr', 'Dr')])
    first_name = StringField(label='First name', validators=[DataRequired()])
    last_name = StringField(label='Last name', validators=[DataRequired()])
    email = EmailField(label='Email address', validators=[DataRequired(), validate_signup_email])
    password = PasswordField(label='Password', validators=[DataRequired(),
                                                           Length(min=8, message='Your password is too short.')])
    password_repeat = PasswordField(label='Repeat Password',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])


class LoginForm(FlaskForm):
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember Me')


def validate_username(self, username):
    username = Profile.query.filter_by(username=username.data).first()
    if username is not None:
        raise ValidationError('The username is already in use.')


class ProfileForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), validate_username])
    photo = FileField('Profile picture', validators=[FileAllowed(photos, 'Images only!')])


class QuestionForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    content = StringField(label='Content', validators=[DataRequired()])
