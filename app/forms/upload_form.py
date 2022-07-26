from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from flask_wtf.file import FileRequired

class UploadForm(FlaskForm):
    image = FileField(validators=[FileRequired()])
    caption  = StringField("Caption")