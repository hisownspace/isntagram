from flask import Blueprint, request
from flask_login import login_required
from app.forms import TagForm
from app.models import db, Tag
from re import match


tag_routes = Blueprint("tags", __name__)

@tag_routes.route("", methods=["POST"])
def create_tag():
    form = TagForm()
    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():

        tag_name = form.data["name"]

        if not match("^[\w]+$", tag_name):
            return { "errors": "Invalid tag name" }

        existing_tag = Tag.query.filter_by(name=tag_name).first()

        if existing_tag and existing_tag.name == tag_name:
            return { "tag": existing_tag.to_dict() }

        tag = Tag(name=tag_name)
        db.session.add(tag)
        db.session.commit()

        return { "tag": tag.to_dict() }

    return { "errors": "Unknown error: Try again later" }

@tag_routes.route("/<string:tag>")
def get_tagged_images(tag):
    tag = Tag.query.filter_by(name=tag)
    print(tag.to_dict())