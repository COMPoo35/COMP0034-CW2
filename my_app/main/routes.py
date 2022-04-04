from flask_login import current_user
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from my_app import photos, db
from my_app.auth.forms import ProfileForm, QuestionForm, AnswerForm
from my_app.models import Profile, User, Question, Answer

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    question = Question.query.order_by(db.text('-question_id')).all()
    return render_template('index.html', question=question)


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_profile = Profile.query.filter_by(profile_username=current_user.username).first()
    if user_profile is None:
        # user profile does not exist, then create profile
        return redirect(url_for('main.create_profile'))
    # user profile exists, then update profile
    return redirect(url_for('main.update_profile'))


@main_bp.route('/post_question', methods=['POST', 'GET'])
@login_required
def post_question():
    question_form = QuestionForm()
    if question_form.validate_on_submit():
        title = question_form.title.data
        content = question_form.content.data
        question = Question(title=title, content=content, question_user_id=current_user.user_id,
                            question_author=current_user.username)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('post_question.html')


@main_bp.route('/question/<int:question_id>', methods=['POST', 'GET'])
@login_required
def post_detail(question_id):
    question = Question.query.get(question_id)
    return render_template('post_detail.html', question=question)


@main_bp.route('/answer/<int:question_id>', methods=['POST', 'GET'])
@login_required
def answer(question_id):
    answer_form = AnswerForm()
    if answer_form.validate_on_submit():
        content = answer_form.content.data
        ans = Answer(content=content, question_id=question_id, answer_user_id=current_user.user_id,
                     answer_author=current_user.username)
        db.session.add(ans)
        db.session.commit()
        return redirect(url_for('main.post_detail', question_id=question_id))
    else:
        flash('Fail to comment!')
        return redirect(url_for('main.post_detail', question_id=question_id))

@main_bp.route('/search')
def search():
    # /search?q=xxx
    q = request.args.get('q')
    question = Question.query.filter(or_(Question.title.contains(q), Question.content.contains(q)))
    return render_template('index.html', question=question)




