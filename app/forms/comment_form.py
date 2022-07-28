from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    content = StringField("content", validators=[DataRequired()])

class DeleteComment(FlaskForm):
    submit = SubmitField()