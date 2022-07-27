from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class TagForm(FlaskForm):
    id = IntegerField("id")
    name = StringField("name", validators=[DataRequired()])
    