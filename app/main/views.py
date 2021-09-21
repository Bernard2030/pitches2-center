from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import ReviewForm, UpdateProfile
from .forms import PitchForm, CommentForm, UpdateProfile
from ..models import Pitch, Comment, User, Upvote, Downvote
from flask_login import login_required,current_user
from .. import db,photos
import markdown2  




# Views

@main.route('/')
@login_required
def index():

    '''
    View root page function that returns the index page and its data

    '''
    # pitch = Pitch.query.all()
    pitch = Pitch.query.order_by(Pitch.date_created.desc()).all()
    business = Pitch.query.filter_by(category='business').all()
    interviews = Pitch.query.filter_by(category='interviews').all()
    products = Pitch.query.filter_by(category='products').all()


   
    return render_template('index.html', business=business, interviews=interviews, products=products, pitch=pitch)

@main.route('/pitch')
@login_required
def pitch():
    Pitch = pitch.query.all()
    likes = Upvote.query.all()
    user = current_user
    return render_template('pitch_display.html', Pitch=Pitch, likes=likes, user=user)

@main.route('/new_Pitch', methods=['GET', 'POST'])
@login_required
def new_Pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        Pitch = form.Pitch.data
        category = form.category.data
        user_id = current_user._get_current_object().id
        Pitch_obj = Pitch(Pitch=Pitch, title=title, category=category, user_id=user_id)
        Pitch_obj.save()
        return redirect(url_for('main.index'))
    return render_template('pitch.html', form=form)

@main.route('/comment/<id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    pitch = Pitch.query.get(id)
    user = User.query.all()
    comment = Comment.query.filter_by(pitch_id=id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        pitch_id = id
        user_id = current_user.id
        new_comment = Comment(
            comment=comment,
            pitch_id=pitch_id,
            user_id=user_id
        )
        new_comment.save()
        new_comment = [new_comment]
        print(new_comment)
        return redirect(url_for('.comment', id =id))
    return render_template('comment.html', form=form, Pitch=Pitch, comment=comment, user=user)



@main.route('/user/<username>', methods = ['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username = username).first()

    if user is None:
        abort(404)

    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        pitch = form.pitch.data
        category = form.category.data
        user_id = current_user.id
        Pitch_obj = Pitch(pitch=pitch, title=title, category=category, user_id=user_id)
        Pitch_obj.save()

    return render_template("profile/profile.html", user = user, form = form)


@main.route('/user/<username>/update',methods = ['GET','POST'])
def update_profile(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',username = user.username))

    return render_template('profile/update.html',form = form)

@main.route('/user/<username>/update/pic',methods = ['POST'])
@login_required
def update_pic(username):
    user = User.query.filter_by(username = username).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',username = username))

@main.route('/like/<int:id>', methods=['GET', 'POST'])
@login_required
def upvote(id):
    Pitch = User.query.get(id)
    vote_new = Upvote(Pitch=Pitch, upvote=1)
    vote_new.save()
    return redirect(url_for('main.Pitchs'))


@main.route('/dislike/<int:id>', methods=['GET', 'POST'])
@login_required
def downvote(id):
    Pitch = User.query.get(id)
    vote = Downvote(Pitch=Pitch, downvote=1)
    vote.save()
    return redirect(url_for('main.Pitchs'))
    