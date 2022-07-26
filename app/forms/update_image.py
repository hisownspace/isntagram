from flask_wtf import FlaskForm
from wtforms import StringField

class UpdateImage(FlaskForm):
    caption = StringField("Caption")