from wtforms import StringField, IntegerField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    content = StringField("content", validators=[DataRequired()])