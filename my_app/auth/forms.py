from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from wtforms import BooleanField
from my_app.models import User


def validate_signup_email(self, email):
    users = User.query.filter_by(email=email.data).first()
    if users is not None:
        raise ValidationError('An account is already registered for that email address')


def validate_username(self, username):
    users = User.query.filter_by(username=username.data).first()
    if users is not None:
        raise ValidationError('A user is already in use')


class SignupForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), validate_username])
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


class QuestionForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    content = StringField(label='Content', validators=[DataRequired()])


class AnswerForm(FlaskForm):
    content = StringField(validators=[DataRequired()])