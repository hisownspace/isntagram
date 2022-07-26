from flask import Blueprint, request
from app.models import db, Image, User
from flask_login import current_user, login_required
from app.s3_helpers import (
    upload_file_to_s3, allowed_file, get_unique_filename)
from app.forms import UploadForm

image_routes = Blueprint("images", __name__)


@image_routes.route("", methods=["POST"])
@login_required
def upload_image():
    form = UploadForm()
    print(form.data)
    if not form.validate_on_submit():
        return { "errors": "There was a problem with the upload." +
                            "Please try again later." }
    if "image" not in request.files:
        return {"errors": "image required"}, 400

    image = request.files["image"]

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
    # flask_login allows us to get the current user from the request
    new_image = Image(user=current_user, url=url)
    db.session.add(new_image)
    db.session.commit()
    return {"url": url}


@image_routes.route("/all")
@login_required
def get_feed():
    this_user_id = 2
    followed_images = []

    following = User.query.get(this_user_id).following
    for user in following:
        for image in user.images:
            followed_images.append(image)
    
    followed_images.sort(key=lambda img: img.created_at, reverse=True)

    return { 
        "followed_images": 
            [image.to_dict() for image in followed_images]
        }

# @image_routes.route("/")