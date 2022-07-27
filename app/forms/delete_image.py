from wtforms import SubmitField
from flask_wtf import FlaskForm


class DeleteImage(FlaskForm):
    submit = SubmitField("submit")