from datetime import datetime

from my_app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    #__table__ = db.Model.metadata.tables['user']

    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    profile_user_id = db.relationship('Profile', backref=db.backref('user'))
    question_user_id = db.relationship('Question', backref=db.backref('user'))


    def __repr__(self):
        return f"{self.user_id} {self.first_name} {self.last_name} {self.email} {self.password}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return (self.user_id)


class Profile(db.Model, UserMixin):
    #__table__ = db.Model.metadata.tables['profile']

    __tablename__ = "profile"
    profile_id = db.Column(db.Integer, primary_key=True, unique=True)
    profile_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    username = db.Column(db.Text)
    photo = db.Column(db.Text)


    def __repr__(self):
        return '<Profile %r>' % self.photo


class Question(db.Model):
    #__table__ = db.Model.metadata.tables['question']

    __tablename__ = "question"
    question_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    question_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


    def __repr__(self):
        return '<Question %r>' % self.title
