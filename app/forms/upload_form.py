from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired, Email, \
                ValidationError
from flask_wtf.file import FileRequired
from app.models import User


class UploadForm(FlaskForm):
    image = FileField(validators=[FileRequired()])
    caption  = StringField("Caption")