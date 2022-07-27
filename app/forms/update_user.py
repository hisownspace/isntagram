from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired


class UpdateUser(FlaskForm):
    email = StringField("email")
    image = FileField("image")
    password = StringField("password")
    username = StringField("username")

class DeleteUser(FlaskForm):
    submit = SubmitField("submit")

# class UpdateUserEmail(FlaskForm):
#     email = StringField("email", validators=[DataRequired()])


# class UpdateUserImage(FlaskForm):
#     image_url = FileField("image", validators=[FileRequired()])


# class UpdateUserPassword(FlaskForm):
#     password = StringField("password", validators=[DataRequired()])


# class UpdateUsername(FlaskForm):
#     username = StringField("username", validators=[DataRequired()])