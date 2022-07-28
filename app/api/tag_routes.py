from flask import Blueprint, request
from flask_login import login_required, current_user
from app.forms import TagForm
from app.models import db, Tag, Image
from app.api.image_routes import image_routes
from re import match


tag_routes = Blueprint("tags", __name__)

@tag_routes.route("", methods=["POST"])
def create_tag():
    form = TagForm()
    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        tags = []

        tag_names = form.data["tags"]
        for tag_name in tag_names:
            if not match("^[\w]+$", tag_name):
                return { "errors": "Invalid tag name" }

            existing_tag = Tag.query.filter_by(name=tag_name).first()

            if existing_tag and existing_tag.name == tag_name:
                return { "tag": existing_tag.to_dict() }

            tag = Tag(name=tag_name)
            db.session.add(tag)
            db.session.commit()
            tags.append(tag)

        return { "tags": [tag.to_dict() for tag in tags] }

    return { "errors": "Unknown error: Try again later" }

@tag_routes.route("/<int:id>")
def get_tagged_images(id):
    tag = Tag.query.get(id)
    tagged_images = tag.to_dict()["images"]
    return { "images": tagged_images}

@tag_routes.route("")
def get_all_tags():
    tags = Tag.query.all()

    return { "tags": [tag.to_dict() for tag in tags] }

# this route uses the url /api/images,
# but was placed here for consistency
@image_routes.route("/<int:id>/tags", methods=["POST", "PUT"])
@login_required
def tag_image(id):
    form = TagForm()
    form["csrf_token"].data = request.cookies["csrf_token"]
    if form.validate_on_submit():
        image = Image.query.get(id)

        if image.user_id != current_user.id:
            return { "errors": "unauthorized resource" }

        ids = form.data["ids"]
        image.tags = []
        for id in ids:
            tag = Tag.query.get(id)
            image.tags.append(tag)
        all_tags = Tag.query.all()
        for tag in all_tags:
            if len(tag.images) == 0:
                db.session.delete(tag)
        db.session.commit()
        return {
                    "image": image.to_dict(), 
                    "tags": [tag.to_dict() for tag in image.tags]
                }
    return { "errors": "Unknown Error. Try again later." }
