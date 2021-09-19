from app.models import Pitch
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField
from wtforms.validators import Required

class ReviewForm(FlaskForm):

    title = StringField('Review title',validators=[Required()])
    review = TextAreaField('Movie review')
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')


class PitchForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    Pitch = TextAreaField('Pitch', validators=[Required()])
    category = SelectField('Category', choices=[('product', 'product'), ('idea', 'idea'), ('business', 'business')],
                           validators=[Required()])
    submit = SubmitField('Pitch')


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('Pitch')


class Vote(FlaskForm):
    submit = SelectField('Like')  

class PitchForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    Pitch = TextAreaField('Pitch', validators=[Required()])
    category = SelectField('Category', choices=[('product', 'product'), ('idea', 'idea'), ('business', 'business')],
                           validators=[Required()])
    submit = SubmitField('Pitch')
