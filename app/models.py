from . import db 
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user
from . import login_manager





#...




class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    Pitch = db.relationship('Pitch', backref='user', lazy="dynamic")

    
   


    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    # @staticmethod
    # def get_user_by_username(username):
    #     return User.query.filter_by(username=username).first()
    

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  
            

    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy = "dynamic")


    def __repr__(self):
        return f'User {self.name}'


        # testing
class Pitch(db.Model):
    __tablename__ = 'pitchs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    pitch = db.Column(db.String, nullable=False)
    comment = db.relationship('Comment', backref='pitch', lazy='dynamic')
    category = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    up_vote = db.relationship('Upvote', backref='pitch', lazy='dynamic')
    down_vote = db.relationship('Downvote', backref='pitch', lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"pitch Title: {self.title}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitchs.id'), nullable=False)
    comment = db.Column(db.Text())

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, pitch_id):
        comments = Comment.query.filter_by(pitch_id=pitch_id).all()
        return comments

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'Comments: {self.comment}' 



class Upvote(db.Model):
    __tablename__ = 'upvotes'
    id = db.Column(db.Integer, primary_key=True)
    upvote = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitchs.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def upvote(cls, id):
        upvote_pitch = Upvote(user=current_user, pitch_id=id)
        upvote_pitch.save()

    @classmethod
    def query_upvotes(cls, id):
        upvote = Upvote.query.filter_by(pitch_id=id).all()
        return upvote

    @classmethod
    def all_upvotes(cls):
        upvotes = Upvote.query.order_by('id').all()
        return upvotes

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'
       

class Downvote(db.Model):
    __tablename__ = 'downvotes'
    id = db.Column(db.Integer, primary_key=True)
    downvote = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitchs.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def downvote(cls, id):
        downvote_pitch = Downvote(user=current_user, pitch_id=id)
        downvote_pitch.save()

    @classmethod
    def query_downvotes(cls, id):
        downvote = Downvote.query.filter_by(pitch_id=id).all()
        return downvote

    @classmethod
    def all_downvotes(cls):
        downvote = Downvote.query.order_by('id').all()
        return downvote

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'



   


        
             




       


 

