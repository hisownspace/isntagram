from flask import Blueprint, request
from app.forms import DeleteImage
from app.forms import TagForm
from app.models import db, Image, User
from flask_login import current_user, login_required
from app.s3_helpers import (
    remove_file_from_s3, upload_file_to_s3, allowed_file, get_unique_filename)
from app.forms import UploadForm, UpdateImage

image_routes = Blueprint("images", __name__)

# User images route is located in user_routes module


@image_routes.route("", methods=["POST"])
@login_required
def upload_image():
    form = UploadForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if not form.validate_on_submit():
        return { "errors": "There was a problem with the upload. " +
                            "Please try again later." }
    if "image" not in form.data:
        return {"errors": "image required"}, 400

    image = form.data["image"]

    if not allowed_file(image.filename):
        return {"errors": "file type not permitted"}, 400
    
    image.filename = get_unique_filename(image.filename)

    upload = upload_file_to_s3(image)

    if "url" not in upload:
        # if the dictionary doesn't have a url key
        # it means that there was an error when we tried to upload
        # so we send back that error message
        return upload, 400

    url = upload["url"]
    caption = form.data["caption"]
    # flask_login allows us to get the current user from the request
    new_image = Image(user=current_user, url=url, caption=caption)
    db.session.add(new_image)
    db.session.commit()
    return { "image": new_image.to_dict() }


@image_routes.route("")
@login_required
def get_feed():

    followed_images = []

    following = User.query.get(current_user.id).following
    for user in following:
        for image in user.images:
            followed_images.append(image)
    
    followed_images.sort(key=lambda img: img.created_at, reverse=True)

    return { 
        "followed_images": 
            [image.to_dict() for image in followed_images]
        }

@image_routes.route("/<int:id>")
def get_image(id):
    image = Image.query.get(id)
    return { "image": image.to_dict() }

@image_routes.route("/<int:id>", methods=["PUT"])
@login_required
def update_image(id):
    if id != current_user.id:
        return { "message": "unauthorized resource" }
    form = UpdateImage()
    image = Image.query.get(id)
    image.caption = form.data["caption"]
    db.session.commit()
    return { "image": image.to_dict() }

@image_routes.route("/<int:id>", methods=["DELETE"])
@login_required
def delete_image(id):
    form = DeleteImage()
    form["csrf_token"].data = request.cookies["csrf_token"]
    if form.validate_on_submit():
        image = Image.query.get(id)
        if image.user_id != current_user.id:
            return { "errors": "unauthorized resource" }
        image_key = image.url.rsplit("/")[-1]
        remove_file_from_s3(image_key)
        db.session.delete(image)
        db.session.commit()
        return { "message": "Delete Successful!" }
    return { "errors": "Unkown error: Try again later." }

@image_routes.route("/<int:id>/tags", methods=["POST"])
def tag_image(id):
    form = TagForm()

    if form.validate_on_submit():
        pass