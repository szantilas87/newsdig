from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed


class NewsForm(FlaskForm):
    title_news = StringField('Title', validators=[DataRequired()])
    text_news = TextAreaField('Description', validators=[DataRequired()])
    picture_link = StringField('Picture Link', validators=[DataRequired()])
    submit_news = SubmitField('Submit')


class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[DataRequired()])
    submit_comment = SubmitField('Submit')


class LikesForm(FlaskForm):
    submit_like = SubmitField('Like')


class DislikesForm(FlaskForm):
    submit_dislike = SubmitField('Dislike')