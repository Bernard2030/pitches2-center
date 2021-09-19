from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import ReviewForm, UpdateProfile
from ..models import Pitch, User
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
    # like = 0
    # dislike = 0
    # like = like, dislike = dislike

  
        
    return render_template('index.html')


@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','Pitch'])
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname = user.username))

    return render_template('profile/update.html',form = form)

@main.route('/user/<uname>/update/pic',methods = ['Pitch'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname = uname))

@main.route('/like/<int:id>', methods=['Pitch', 'GET'])
@login_required
def upvote(id):
    Pitch = Pitch.query.get(id)
    vote_mpya = Upvote(Pitch=Pitch, upvote=1)
    vote_mpya.save()
    return redirect(url_for('main.Pitchs'))


@main.route('/dislike/<int:id>', methods=['GET', 'Pitch'])
@login_required
def downvote(id):
    Pitch = Pitch.query.get(id)
    vm = Downvote(Pitch=Pitch, downvote=1)
    vm.save()
    return redirect(url_for('main.Pitchs'))
    