from datetime import datetime

from my_app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    # __table__ = db.Model.metadata.tables['user']

    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    profiles = db.relationship('Profile', backref=db.backref('user'))
    questions = db.relationship('Question', backref=db.backref('user'))
    #answers = db.relationship('Answer', backref='user')

    def __repr__(self):
        return f"{self.user_id} {self.username} {self.first_name} {self.last_name} {self.email} {self.password}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return (self.user_id)


class Question(db.Model):
    # __table__ = db.Model.metadata.tables['question']

    __tablename__ = "question"
    question_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    question_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    question_author = db.Column(db.Text)
    #answer_question_id = db.relationship('Question', backref='question')

    def __repr__(self):
        return '<Question %r>' % self.title

class Answer(db.Model):
    __tablename__ = "answer"
    answer_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'))
    answer_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    answer_author = db.Column(db.Text)

    question = db.relationship('Question', backref='answers')
    author = db.relationship('User', backref='answers')


