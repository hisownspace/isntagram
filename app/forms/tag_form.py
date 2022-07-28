from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList

class TagForm(FlaskForm):
    ids = FieldList(IntegerField("ids"))
    tags = FieldList(StringField("tags"))
    