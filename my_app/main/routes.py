from flask_login import current_user
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from my_app import photos, db
from my_app.auth.forms import ProfileForm, QuestionForm
from my_app.models import Profile, User, Question

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    question = Question.query.all()
    return render_template('index.html', question=question)


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_profile = Profile.query.filter_by(profile_user_id=current_user.user_id).first()
    if user_profile is None:
        # user profile does not exist, then create profile
        return redirect(url_for('main.create_profile'))
    # user profile exists, then update profile
    return redirect(url_for('main.update_profile'))


@main_bp.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    form = ProfileForm()  # This should be familiar from login and signup routes in auth
    if request.method == 'POST' and form.validate_on_submit():
        filename = None  # Set the filename for the photo to None since this is the default if the user hasn't chosen to add a profile photo
        if 'photo' in request.files:  # Let's you check the submited form contains a photo (photo is the field name we used in the ProfileForm class)
            if request.files['photo'].filename != '':  # As long as the filename isn't empty then save the photo
                filename = photos.save(request.files[
                                           'photo'])  # This saves the photo using the global variable photos to get the location to save to
        p = Profile(username=form.username.data, photo=filename,
                    profile_user_id=current_user.user_id)  # Build a new profile to be added to the database based on the fields in the form
        try:
            db.session.add(p)  # Add the new Profile to the database session
            db.session.commit()  # This saves the new Profile to the database
            flash('Profile is successfully created.')
        except IntegrityError:
            db.session.rollback()
            flash('Error, unable to create the profile.')
            return redirect(url_for('main.profile'))
        return redirect(url_for('main.display_profile'))
    return render_template('profile.html', form=form)


@main_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    profile = Profile.query.join(User, User.user_id == Profile.profile_user_id). \
        filter_by(user_id=current_user.user_id).first()
    form = ProfileForm(obj=profile)
    if request.method == 'POST' and form.validate_on_submit():
        if 'photo' in request.files:
            if request.files['photo'].filename != '':
                filename = photos.save(request.files['photo'])
                profile.photo = filename  # Updates the photo field
        profile.username = form.username.data
        db.session.commit()  # Save the changes to the database
        return redirect(url_for('main.display_profile', username=profile.username))
    return render_template('profile.html', form=form)


@main_bp.route('/display_profile', methods=['POST', 'GET'])
@main_bp.route('/display_profile/<username>/', methods=['POST', 'GET'])
@login_required
def display_profile(username=None):
    results = None
    if username is None:
        if request.method == 'POST':
            term = request.form['search_term']
            if term == "":
                flash("Enter a name to search for")
                return redirect(url_for("main.index"))
            results = Profile.query.filter(Profile.username.contains(term)).all()
    else:
        results = Profile.query.filter_by(username=username).all()
    if not results:
        flash("No users found.")
        return redirect(url_for("main.index"))
    # The following iterates through the results and adds the full url to a list of urls
    urls = []
    for result in results:
        url = photos.url(
            result.photo)  # uses the global photos plus the photo file name to determine the full url path
        urls.append(url)
    return render_template('display_profile.html',
                           profiles=zip(results, urls))  # Note the zip to pass both lists as a parameter


@main_bp.route('/post_question', methods=['POST', 'GET'])
@login_required
def post_question():
    question_form = QuestionForm()
    if question_form.validate_on_submit():
        title = question_form.title.data
        content = question_form.content.data
        question = Question(title=title, content=content, question_user_id=current_user.user_id)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('post_question.html')
